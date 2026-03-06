using System;
using System.IO;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using _OCPP.DataTypes;
using Control.CSMS;
using Vector.Tools;

namespace UserDefinedLibrary
{

	class CryptoUtils
	{
		public static string GetCertificateAsString(string filename)
		{
			try
			{
				return File.ReadAllText(filename);
			}
			catch (Exception e)
			{
				Utils.WriteError(e.Message);
				return "";
			}
		}
		public static string GetHashAlgorithm(X509Certificate2 certificate)
		{
			return certificate.SignatureAlgorithm.FriendlyName;
		}

		// only works for selfsigned certificates
		public static string GetIssuerKeyHash(X509Certificate2 certificate)
		{
			using (var sha256 = SHA256.Create())
			{
				byte[] issuerKeyBytes = certificate.GetPublicKey();
				byte[] hashBytes = sha256.ComputeHash(issuerKeyBytes);
				return BitConverter.ToString(hashBytes).Replace("-", "").ToLower();
			}
		}
		public static string GetIssuerNameHash(X509Certificate2 certificate)
		{
			using (var sha256 = SHA256.Create())
			{
				byte[] issuerNameBytes = certificate.IssuerName.RawData;
				byte[] hashBytes = sha256.ComputeHash(issuerNameBytes);
				return BitConverter.ToString(hashBytes).Replace("-", "").ToLower();
			}
		}

		public static string GetSubjectNameHash(X509Certificate2 certificate)
		{
			using (var sha256 = SHA256.Create())
			{
				byte[] subjectNameBytes = certificate.SubjectName.RawData;
				byte[] hashBytes = sha256.ComputeHash(subjectNameBytes);
				return BitConverter.ToString(hashBytes).Replace("-", "").ToLower();
			}
		}

		public static string DummyCSR()
		{
			// Generate a key pair
			using (RSA rsa = RSA.Create(2048))
			{
				var request = new CertificateRequest("CN=DummyV2G", rsa, HashAlgorithmName.SHA512, RSASignaturePadding.Pkcs1);

				// Add extensions (optional)
				request.CertificateExtensions.Add(new X509KeyUsageExtension(X509KeyUsageFlags.DigitalSignature, false));

				// Create the CSR
				byte[] csr = request.CreateSigningRequest();

				// Convert CSR to Base64
				string csrBase64 = Convert.ToBase64String(csr);
				Console.WriteLine("CSR:");
				Console.WriteLine(csrBase64);

				return csrBase64;
			}
		}

		public static void InterpretCSR(string csr)
		{
			var csrBytes = Convert.FromBase64String(csr);
			var request = CertificateRequest.LoadSigningRequest(csrBytes, HashAlgorithmName.SHA512);
			var subject = request.SubjectName.Name;
			var publicKey = request.PublicKey;
			var hashAlg = request.HashAlgorithm;

			Utils.WriteLine("CSR interpretation", "Subject: " + subject);
			Utils.WriteLine("CSR interpretation", "Public Key: " + Convert.ToBase64String(publicKey.EncodedKeyValue.RawData));
			Utils.WriteLine("CSR interpretation", $"Hash Alg: {hashAlg}");

		}

		public static string DER_cert_string_to_PEM_cert(string certificateDERString)
		{
			byte[] certificateDERBytes = Convert.FromBase64String(certificateDERString);
			return DER_cert_to_PEM_cert(certificateDERBytes);
		}

		public static string DER_cert_to_PEM_cert(byte [] certificateDERBytes)
		{
			string pemCertString;
			string base64Cert = Convert.ToBase64String(certificateDERBytes, Base64FormattingOptions.InsertLineBreaks);
			
			// Add PEM headers and footers
			pemCertString = "-----BEGIN CERTIFICATE-----\n" + base64Cert + "\n-----END CERTIFICATE-----";

			return pemCertString;
		}
	}

	class Utils
	{
		/// <summary>
		/// Output current path to the write panel
		/// </summary>
		public static void OutputCurrentPath()
		{
			Output.WriteLine($"Current path: {Directory.GetCurrentDirectory()}");
		}

		/// <summary>
		/// Cat the outputs of a file to the write panel
		/// </summary>
		public static void Cat(string filename)
		{
			try
			{
				string[] lines = File.ReadAllLines(filename);
				foreach (string line in lines)
				{
					Output.WriteLine(line);
				}
			}
			catch (Exception e)
			{
				Output.WriteLine("An error occurred: " + e.Message);
			}
		}

		public static void WriteLine(string prefix, string s)
		{
			Output.WriteLine($"[{prefix}]: {s}");
		}

		public static void WriteError(string s)
		{
			Output.WriteLine($"[Error]: {s}");
		}
	}

  class ChargingStation_State
  {
    public static bool IsOCPP16()
    {
      return Common.SysSelectedProtocol.Value == Common.OCPPVersions_SysSelectedProtocol.OCPP_16;
    }

    public static bool IsOCPP201()
    {
      return Common.SysSelectedProtocol.Value == Common.OCPPVersions_SysSelectedProtocol.OCPP_201;
    }
    
    public static bool IsOCPP21()
    {
      return Common.SysSelectedProtocol.Value ==  Common.OCPPVersions_SysSelectedProtocol.OCPP_21;
    }
  }

  class CSMS_State
  {
    public static bool IsOCPP16()
    {
      return Common.SysSelectedProtocol.Value == Common.OCPPVersions_SysSelectedProtocol.OCPP_16;
    }

    public static bool IsOCPP201()
    {
      return Common.SysSelectedProtocol.Value == Common.OCPPVersions_SysSelectedProtocol.OCPP_201;
    }
    
    public static bool IsOCPP21()
    {
      return Common.SysSelectedProtocol.Value == Common.OCPPVersions_SysSelectedProtocol.OCPP_21;
    }
  }

	class UserCertificate
	{
		public UserCertificate(byte[] certificateDERBytes)
		{
			try
			{
				var cert = new X509Certificate2(certificateDERBytes);

				hashAlg = CryptoUtils.GetHashAlgorithm(cert);
				issuerNameHash = CryptoUtils.GetIssuerNameHash(cert);
				issuerKeyHash = CryptoUtils.GetIssuerKeyHash(cert);
				serialNumber = cert.SerialNumber;
				subjectNameHash = CryptoUtils.GetSubjectNameHash(cert);

				certPEMString = CryptoUtils.DER_cert_to_PEM_cert(certificateDERBytes);
				
				// Print the values
				Utils.WriteLine("Certificate", $"Hash Algorithm: {hashAlg}");
				Utils.WriteLine("Certificate", $"Issuer Name Hash: {issuerNameHash}");
				Utils.WriteLine("Certificate", $"Subject Name Hash: {subjectNameHash}");
				Utils.WriteLine("Certificate", $"Public Key hash: {issuerKeyHash}");
				Utils.WriteLine("Certificate", $"Serial Number: {serialNumber} \n");
			}
			catch (Exception e)
			{
				throw new Exception($"Invalid parsing of user certificate with: {e.Message.Replace("\n", "")}");
			}
		}

		public const string V2G_CERTIFICATE_TYPE = "V2GRootCertificate";

		public string hashAlg { get; set; }
		public string issuerNameHash { get; set; }
		public string issuerKeyHash { get; set; }
		public string serialNumber { get; set; }
		public string certPEMString { get; set; }
		public string subjectNameHash { get; set; }

	}

	class MessageHelper
	{
		public static SetVariableData SetVariableBuilder(Custom_TypeComponent? typeComponent, Custom_Status? status)
		{
			var r = SetVariableData.CreateInstance();

			r.attributeType.Assign("Actual");
			r.variable.name = "Enabled";


			switch (typeComponent)
			{
				case Custom_TypeComponent.AuthCtrlr:
					r.component.name = "AuthCtrlr";
					break;
			}

			switch (status)
			{
				case Custom_Status.Enable:
					r.attributeValue = "true";
					break;

				case Custom_Status.Disable:
					r.attributeValue = "false";
					break;
			}

			return r;
		}
		public static void UpdateCertificateHashData16(CertificateHashData16 data, UserCertificate c)
		{
			data.hashAlgorithm = c.hashAlg;
			data.issuerNameHash = c.issuerNameHash;
			data.issuerKeyHash = c.issuerKeyHash;
			data.serialNumber = c.serialNumber;
		}

		public static void UpdateCertificateHashData201(CertificateHashData201 data, UserCertificate c)
		{
			data.hashAlgorithm = c.hashAlg;
			data.issuerNameHash = c.issuerNameHash;
			data.issuerKeyHash = c.issuerKeyHash;
			data.serialNumber = c.serialNumber;
		}

		public static void UpdateCertificateHashData21(CertificateHashData201 data, UserCertificate c)
		{
			data.hashAlgorithm = c.hashAlg;
			data.issuerNameHash = c.issuerNameHash;
			data.issuerKeyHash = c.issuerKeyHash;
			data.serialNumber = c.serialNumber;
		}
	}
}
