using UnityEngine;

public class CabinPanoramaViewController : MonoBehaviour
{
    [Header("Input")]
    public UdpUiRenderReceiver receiver;

    [Header("Ambient Zones")]
    public Renderer[] ambientZoneRenderers;

    [Header("IC Flow Indicators (0..7)")]
    public GameObject[] flowPhaseIndicators;

    [Header("Direction Arrows (0=None 1=Left 2=Right 3=Rear)")]
    public GameObject leftArrow;
    public GameObject rightArrow;
    public GameObject rearArrow;

    private Material[] _ambientMaterials;

    private void Start()
    {
        if (receiver == null)
        {
            Debug.LogWarning("[CabinPanoramaViewController] receiver is not assigned.");
            return;
        }

        _ambientMaterials = new Material[ambientZoneRenderers == null ? 0 : ambientZoneRenderers.Length];
        for (int i = 0; i < _ambientMaterials.Length; i++)
        {
            if (ambientZoneRenderers[i] != null)
            {
                _ambientMaterials[i] = ambientZoneRenderers[i].material;
            }
        }

        receiver.PacketUpdated += OnPacketUpdated;
    }

    private void OnDestroy()
    {
        if (receiver != null)
        {
            receiver.PacketUpdated -= OnPacketUpdated;
        }
    }

    private void OnPacketUpdated(UiRenderPacket packet)
    {
        UiRenderState s = packet.uiRender;
        if (s == null)
        {
            return;
        }

        ApplyAmbient(s);
        ApplyFlowPhase(s);
        ApplyDirection(s);
    }

    private void ApplyAmbient(UiRenderState s)
    {
        if (_ambientMaterials == null)
        {
            return;
        }

        Color c = UiRenderVisualMap.AmbientColor(s.renderColor, s.ambientPulsePhase);
        for (int i = 0; i < _ambientMaterials.Length; i++)
        {
            if (_ambientMaterials[i] != null)
            {
                _ambientMaterials[i].color = c;
            }
        }
    }

    private void ApplyFlowPhase(UiRenderState s)
    {
        if (flowPhaseIndicators == null || flowPhaseIndicators.Length == 0)
        {
            return;
        }

        int index = Mathf.Clamp(s.icFlowPhase, 0, flowPhaseIndicators.Length - 1);
        for (int i = 0; i < flowPhaseIndicators.Length; i++)
        {
            if (flowPhaseIndicators[i] != null)
            {
                flowPhaseIndicators[i].SetActive(i == index);
            }
        }
    }

    private void ApplyDirection(UiRenderState s)
    {
        if (leftArrow != null) leftArrow.SetActive(s.renderDirection == 1);
        if (rightArrow != null) rightArrow.SetActive(s.renderDirection == 2);
        if (rearArrow != null) rearArrow.SetActive(s.renderDirection == 3);
    }
}
