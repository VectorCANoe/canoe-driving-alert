using System;
using Vector.CANoe.Runtime;

using UserDefinedLibrary;

public class SecurityNode : MeasurementScript
{
    /// <summary>
    /// Called before measurement start to perform necessary initializations,
    /// e.g. to create objects. During measurement, few additional objects
    /// should be created to prevent garbage collection runs in time-critical
    /// simulations.
    /// </summary>
    public override void Initialize()
    {
    }

    /// <summary>Notification that the measurement starts.</summary>
    public override void Start()
    {
    }

    /// <summary>Notification that the measurement ends.</summary>
    public override void Stop()
    {
    }

    /// <summary>
    /// Cleanup after the measurement. Complement to Initialize. This is not
    /// a "Dispose" method; your object should still be usable afterwards.
    /// </summary>
    public override void Shutdown()
    {
    }

    [OnChange(typeof(Control.CSMS.SendInstallCertificateRequest))]
    public void SendInstallCertificateRequestCallback()
    {
        if (Control.CSMS.SendInstallCertificateRequest.Value == 1)
        {
            // get from system variable the 
            var certificate_der = Security.SysDEREncodedCertificate.Value;

            if (certificate_der.Length < 0)
            {
                Utils.WriteError("No certificate Loaded");
                return;
            }

            try
            {
                Utils.WriteLine("Certificate", "Sending InstallCertificate with: ");
                var certificate = new UserCertificate(certificate_der);

                if (CSMS_State.IsOCPP16())
                {
                    OCPP.Simulation.CSMS.OCPP16.InstallCertificateRequest.certificateType = UserCertificate.V2G_CERTIFICATE_TYPE;
                    OCPP.Simulation.CSMS.OCPP16.InstallCertificateRequest.certificate = certificate.certPEMString;
                }
                else if (CSMS_State.IsOCPP201())
                {
                    OCPP.Simulation.CSMS.OCPP201.InstallCertificateRequest.certificateType = UserCertificate.V2G_CERTIFICATE_TYPE;
                    OCPP.Simulation.CSMS.OCPP201.InstallCertificateRequest.certificate = certificate.certPEMString;
                }
                else if (CSMS_State.IsOCPP21())
                {
                    OCPP.Simulation.CSMS.OCPP21.InstallCertificateRequest.certificateType = UserCertificate.V2G_CERTIFICATE_TYPE;
                    OCPP.Simulation.CSMS.OCPP21.InstallCertificateRequest.certificate = certificate.certPEMString;
                }
                else
                {
                    Utils.WriteError("Invalid OCPP version selected. Selected function can not be used.");
                }
            }
            catch (Exception e)
            {
                Utils.WriteError(e.Message);
            }
        }
    }

    [OnChange(typeof(Control.CSMS.SendDeleteCertificateRequest))]
    public void SendDeleteCertificateRequestCallback()
    {
        // check if button is in the "pressed" state
        if (Control.CSMS.SendDeleteCertificateRequest.Value == 1)
        {
            // get from system variable the 
            var certificate_der = Security.SysDEREncodedCertificate.Value;

            if (certificate_der.Length < 0)
            {
                Utils.WriteError("No certificate Loaded");
                return;
            }

            try
            {
                Utils.WriteLine("Certificate", "Sending DeleteInstallCertificate with: ");
                var certificate = new UserCertificate(certificate_der);

                if (CSMS_State.IsOCPP16())
                {
                    MessageHelper.UpdateCertificateHashData16(OCPP.Simulation.CSMS.OCPP16.DeleteCertificateRequest.certificateHashData, certificate);
                }
                else if (CSMS_State.IsOCPP201())
                {
                    MessageHelper.UpdateCertificateHashData201(OCPP.Simulation.CSMS.OCPP201.DeleteCertificateRequest.certificateHashData, certificate);
                }
                else if (CSMS_State.IsOCPP21())
                {
                    MessageHelper.UpdateCertificateHashData21(OCPP.Simulation.CSMS.OCPP21.DeleteCertificateRequest.certificateHashData, certificate);
                }
                else
                {
                    Utils.WriteError("Invalid OCPP version selected. Selected function can not be used.");
                }
            }
            catch
            {
                Utils.WriteError("No certificate loaded");
            }
        }
    }


    [OnChange(typeof(Control.CSMS.SendVariableRequest))]
    public void SendVariableRequestCallback()
    {
        if (Control.CSMS.SendVariableRequest.Value == 1)
        {
            if (CSMS_State.IsOCPP201())
            {
                OCPP.Simulation.CSMS.OCPP201.SetVariablesRequest.setVariableData[0].Assign(MessageHelper.SetVariableBuilder(Control.CSMS.TypeComponent.Value, Control.CSMS.Status.Value));
            }
            else if (CSMS_State.IsOCPP21())
            {
                OCPP.Simulation.CSMS.OCPP21.SetVariablesRequest.setVariableData[0].Assign(MessageHelper.SetVariableBuilder(Control.CSMS.TypeComponent.Value, Control.CSMS.Status.Value));
            }
            else
            {
                Utils.WriteError("Invalid OCPP version selected. Selected function can not be used.");
            }
        }
    }

    [OnChange(typeof(Control.CSMS.SysSendTriggerMessageReq))]
    public void SendTriggerMessageReqCallback()
    {
        if (Control.CSMS.SysSendTriggerMessageReq.Value == 1)
        {
            if (CSMS_State.IsOCPP16())
            {
                OCPP.Simulation.CSMS.OCPP16.TriggerMessageRequest.requestedMessage = "SignV2GCertificate";
            }
            else if (CSMS_State.IsOCPP201())
            {
                OCPP.Simulation.CSMS.OCPP201.TriggerMessageRequest.requestedMessage = "SignV2GCertificate";
            }
            else if (CSMS_State.IsOCPP21())
            {
                OCPP.Simulation.CSMS.OCPP21.TriggerMessageRequest.requestedMessage = "SignV2GCertificate";
            }
            else
            {
                Utils.WriteError("Invalid OCPP version selected. Selected function can not be used.");
            }
        }
    }

    [OnChange(OCPP.Simulation.ChargingStation.MemberIDs.OCPP16.TriggerMessageRequest)]
    public void TriggerMessageRequestCallbackOCPP16()
    {
        if (OCPP.Simulation.ChargingStation.OCPP16.TriggerMessageRequest.requestedMessage == "SignV2GCertificate")
        {
            Utils.WriteLine("TriggeredMessage", "Sending SignCertificateRequest");
            OCPP.Simulation.ChargingStation.OCPP16.SignCertificateRequest.csr = CryptoUtils.DummyCSR();
        }
    }

    [OnUpdate(OCPP.Simulation.ChargingStation.MemberIDs.OCPP201.TriggerMessageRequest)]
    public void TriggerMessageRequestCallbackOCPP201()
    {
        if (OCPP.Simulation.ChargingStation.OCPP201.TriggerMessageRequest.requestedMessage == "SignV2GCertificate")
        {
            Utils.WriteLine("TriggeredMessage", "Sending SignCertificateRequest");
            OCPP.Simulation.ChargingStation.OCPP201.SignCertificateRequest.csr = CryptoUtils.DummyCSR();
            OCPP.Simulation.ChargingStation.OCPP201.SignCertificateRequest.certificateType.Assign("V2GCertificate");
        }
    }

    [OnUpdate(OCPP.Simulation.CSMS.MemberIDs.OCPP201.SignCertificateRequest)]
    public void SignCertificateRequest201CallBack()
    {
        // CryptoUtils.InterpretCSR(OCPP.Simulation.CSMS.OCPP201.SignCertificateRequest.csr);

        // convert from base64 String to bytes
        var bytesCSR = Convert.FromBase64String(OCPP.Simulation.CSMS.OCPP201.SignCertificateRequest.csr);

        Security.SysCSR.Value = bytesCSR;
    }

    [OnUpdate(OCPP.Simulation.CSMS.MemberIDs.OCPP16.SignCertificateRequest)]
    public void SignCertificateRequest16CallBack()
    {
        // CryptoUtils.InterpretCSR(OCPP.Simulation.CSMS.OCPP201.SignCertificateRequest.csr);

        // convert from base64 String to bytes
        var bytesCSR = Convert.FromBase64String(OCPP.Simulation.CSMS.OCPP16.SignCertificateRequest.csr);

        Security.SysCSR.Value = bytesCSR;
    }

    [OnChange(typeof(Security.CSR.SysCert_DER))]
    public void CertFromCSR_DER_Callback()
    {
        Utils.WriteLine("Certificate", "Newly created certificate from CSR");
        var bytesCert = Convert.FromHexString(Security.CSR.SysCert_DER.Value);
        try
        {
            var c = new UserCertificate(bytesCert);
            var certChain = CertificateChainCreation();

            if (CSMS_State.IsOCPP16())
            {
                OCPP.Simulation.CSMS.OCPP16.CertificateSignedRequest.certificateChain = certChain;
            }
            else if (CSMS_State.IsOCPP201())
            {
                OCPP.Simulation.CSMS.OCPP201.CertificateSignedRequest.certificateType.Value = Security.CSR.SysCertificateType.Value;
                OCPP.Simulation.CSMS.OCPP201.CertificateSignedRequest.certificateChain = certChain;
            }
            else if (CSMS_State.IsOCPP21())
            {
                OCPP.Simulation.CSMS.OCPP21.CertificateSignedRequest.certificateType.Value = Security.CSR.SysCertificateType.Value;
                OCPP.Simulation.CSMS.OCPP21.CertificateSignedRequest.certificateChain = certChain;
            }
            else
            {
                Utils.WriteError("Invalid OCPP version selected. Selected function can not be used.");
            }
        }
        catch
        {
            Utils.WriteError("Error when loading certificate");
        }

    }

    public static string CertificateChainCreation()
    {
        Utils.WriteLine("CertChain", "Now constructing certificate chain");
        string certChain = "";
        try
        {
            var certFromCSR_DER = Convert.FromHexString(Security.CSR.SysCert_DER.Value);
            var sub2Cert_DER = Convert.FromHexString(Security.CSR.SysSub2Cert_DER.Value);
            var sub1Cert_DER = Convert.FromHexString(Security.CSR.SysSub1Cert_DER.Value);

            var certFromCSR_PEM = CryptoUtils.DER_cert_to_PEM_cert(certFromCSR_DER);
            var sub2Cert_PEM = CryptoUtils.DER_cert_to_PEM_cert(sub2Cert_DER);
            var sub1Cert_PEM = CryptoUtils.DER_cert_to_PEM_cert(sub1Cert_DER);
            certChain = certFromCSR_PEM + sub2Cert_PEM + sub1Cert_PEM;
        }
        catch (Exception ex)
        {
            Utils.WriteError(ex.Message);
        }

        return certChain;
    }
}
