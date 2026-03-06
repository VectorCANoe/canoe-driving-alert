using UnityEngine;

public class UiRenderStatusOverlay : MonoBehaviour
{
    public UdpUiRenderReceiver receiver;
    public bool showOverlay = true;
    public int fontSize = 16;
    public int width = 420;
    public int height = 210;
    public Vector2 topLeft = new Vector2(20, 20);

    private GUIStyle _labelStyle;
    private Texture2D _bgTex;

    private void Start()
    {
        if (receiver == null)
        {
            receiver = FindObjectOfType<UdpUiRenderReceiver>();
        }

        _labelStyle = new GUIStyle(GUI.skin.label);
        _labelStyle.fontSize = fontSize;
        _labelStyle.normal.textColor = Color.white;

        _bgTex = new Texture2D(1, 1);
        _bgTex.SetPixel(0, 0, new Color(0f, 0f, 0f, 0.65f));
        _bgTex.Apply();
    }

    private void OnGUI()
    {
        if (!showOverlay || receiver == null || !receiver.hasValidPacket)
        {
            return;
        }

        Rect rect = new Rect(topLeft.x, topLeft.y, width, height);
        GUI.DrawTexture(rect, _bgTex);

        UiRenderState s = receiver.current;
        if (s == null)
        {
            return;
        }

        float line = topLeft.y + 10;
        float x = topLeft.x + 12;

        DrawLine(x, ref line, $"seq={receiver.lastSeq} tsMs={receiver.lastTsMs}");
        DrawLine(x, ref line, $"mode={s.renderMode} color={s.renderColor} pattern={s.renderPattern}");
        DrawLine(x, ref line, $"textCode={s.renderTextCode} direction={s.renderDirection}");
        DrawLine(x, ref line, $"zoneColor={s.roadZoneColorCode} flowDir={s.roadFlowDirection} icPhase={s.icFlowPhase}");
        DrawLine(x, ref line, $"vehiclePos={s.vehicleObjectPos} emsPhase={s.emsBlinkPhase} pulse={s.ambientPulsePhase}");
        DrawLine(x, ref line, $"activeAlertType={s.activeAlertType}");
    }

    private void DrawLine(float x, ref float y, string text)
    {
        GUI.Label(new Rect(x, y, width - 20, 28), text, _labelStyle);
        y += 28;
    }
}
