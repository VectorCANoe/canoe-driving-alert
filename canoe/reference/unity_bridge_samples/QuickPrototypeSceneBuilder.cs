using UnityEngine;

public class QuickPrototypeSceneBuilder : MonoBehaviour
{
    public enum BuildMode
    {
        ExternalOnly,
        CabinOnly,
        Both
    }

    [Header("Build")]
    public BuildMode mode = BuildMode.Both;
    public bool buildOnStart = true;
    public bool clearExistingNamedObjects = false;

    private void Start()
    {
        if (buildOnStart)
        {
            Build();
        }
    }

    [ContextMenu("Build Prototype Scene")]
    public void Build()
    {
        if (clearExistingNamedObjects)
        {
            CleanupNamedObjects();
        }

        if (mode == BuildMode.ExternalOnly || mode == BuildMode.Both)
        {
            BuildExternal();
        }

        if (mode == BuildMode.CabinOnly || mode == BuildMode.Both)
        {
            BuildCabin();
        }
    }

    private void CleanupNamedObjects()
    {
        string[] names = new string[]
        {
            "RoadLane","FlowStrip","VehicleMarker","EmergencyLightLeft","EmergencyLightRight",
            "AmbientZone_Driver","AmbientZone_Passenger","AmbientZone_Rear",
            "DirectionArrow_Left","DirectionArrow_Right","DirectionArrow_Rear"
        };

        foreach (string n in names)
        {
            GameObject go = GameObject.Find(n);
            if (go != null)
            {
                Destroy(go);
            }
        }

        for (int i = 0; i < 8; i++)
        {
            GameObject phase = GameObject.Find("FlowPhase_" + i);
            if (phase != null)
            {
                Destroy(phase);
            }
        }
    }

    private void BuildExternal()
    {
        CreateCube("RoadLane", new Vector3(0f, 0f, 0f), new Vector3(10f, 0.2f, 2f), new Color(0.65f, 0.67f, 0.70f, 1f));
        CreateCube("FlowStrip", new Vector3(0f, 0.2f, -0.9f), new Vector3(10f, 0.05f, 0.2f), new Color(0.22f, 0.86f, 0.68f, 1f));
        CreateSphere("VehicleMarker", new Vector3(-5f, 0.5f, 0f), 0.4f, new Color(0.9f, 0.9f, 0.95f, 1f));
        CreateSphere("EmergencyLightLeft", new Vector3(4.0f, 0.7f, 0.5f), 0.25f, Color.red);
        CreateSphere("EmergencyLightRight", new Vector3(4.6f, 0.7f, 0.5f), 0.25f, Color.blue);
    }

    private void BuildCabin()
    {
        CreateCube("AmbientZone_Driver", new Vector3(-3f, 2.5f, 2f), new Vector3(2.2f, 0.25f, 0.4f), new Color(0.2f, 0.82f, 0.72f, 1f));
        CreateCube("AmbientZone_Passenger", new Vector3(0f, 2.5f, 2f), new Vector3(2.2f, 0.25f, 0.4f), new Color(0.2f, 0.82f, 0.72f, 1f));
        CreateCube("AmbientZone_Rear", new Vector3(3f, 2.5f, 2f), new Vector3(2.2f, 0.25f, 0.4f), new Color(0.2f, 0.82f, 0.72f, 1f));

        for (int i = 0; i < 8; i++)
        {
            Color c = i == 0 ? new Color(0.95f, 0.78f, 0.16f, 1f) : new Color(0.15f, 0.15f, 0.15f, 1f);
            CreateCube("FlowPhase_" + i, new Vector3(-3.5f + i, 1.9f, 2f), new Vector3(0.7f, 0.2f, 0.2f), c);
        }

        CreateCube("DirectionArrow_Left", new Vector3(-4.5f, 2.1f, 2f), new Vector3(0.5f, 0.3f, 0.2f), new Color(0.2f, 0.43f, 0.94f, 1f));
        CreateCube("DirectionArrow_Right", new Vector3(4.5f, 2.1f, 2f), new Vector3(0.5f, 0.3f, 0.2f), new Color(0.2f, 0.43f, 0.94f, 1f));
        CreateCube("DirectionArrow_Rear", new Vector3(0f, 1.3f, 2f), new Vector3(0.5f, 0.3f, 0.2f), new Color(0.2f, 0.43f, 0.94f, 1f));
    }

    private static void CreateCube(string name, Vector3 position, Vector3 scale, Color color)
    {
        GameObject existing = GameObject.Find(name);
        if (existing != null)
        {
            return;
        }

        GameObject go = GameObject.CreatePrimitive(PrimitiveType.Cube);
        go.name = name;
        go.transform.position = position;
        go.transform.localScale = scale;
        SetColor(go, color);
    }

    private static void CreateSphere(string name, Vector3 position, float radius, Color color)
    {
        GameObject existing = GameObject.Find(name);
        if (existing != null)
        {
            return;
        }

        GameObject go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        go.name = name;
        go.transform.position = position;
        go.transform.localScale = new Vector3(radius, radius, radius);
        SetColor(go, color);
    }

    private static void SetColor(GameObject go, Color c)
    {
        Renderer r = go.GetComponent<Renderer>();
        if (r != null)
        {
            r.material.color = c;
        }
    }
}
