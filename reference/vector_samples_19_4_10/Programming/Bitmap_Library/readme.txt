Description Bitmap Library
**********************************
In the Bitmap Library you will find a collection of images that can be
used for panel design.

The contained images can be used for the Switch/Indicator Control.The library is structured according to the number of states represented on the images.

Please copy all images you intend to use into your corresponding CANoe/CANalyzer project folder before using them. You can then link the controls with the desired 
image in the Panel Designer.
 
The name of the images is composed as follows:
<Name>_n.png
n = number of states (n>=2)
for example: LightABS_2.png


**Note: Display states with LEDs**
If you want to use an LED, for example, to represent a lamp that can be switched on 
and off, use the LED Control in the Panel Designer.
You can assign individual colors to each state. Both, the number of states as well as the shape of the LED, is configurable.

Example 1: map a green LED
 LED Control:
  State 0; Value 0; Color: gray
  State 1; Value 1; Color: green

Example 2: map an LED that has the traffic light colors
 LED Control:
  State 0; Value 0; Color: red
  State 1; Value 1; Color: yellow
  State 2; Value 2; Color: green


Beschreibung Bitmap Library
**********************************
In der Bitmap Library finden Sie eine Zusammenstellung von Bildern, die fuer die Panelgestaltung
verwendet werden koennen. 

Hier enthaltene Bilder sind verwendbar fuer das Switch/Indicator Control im Panel Designer, bei dem Bilder 
konfiguriert werden koennen. 
Die Bibliothek ist strukturiert nach Anzahl der Zustaende, die auf den Bildern dargestellt sind.

Bilder, die Sie in Ihren Panels verwenden moechten, kopieren Sie zuvor in das Verzeichnis der 
entsprechenden CANoe/CANalyzer-Konfiguration. Anschliessend koennen Sie im Panel Designer die Steuerelemente mit
dem gewuenschten Bild verknuepfen.

Die Bezeichnung der Bilder setzt sich folgendermassen zusammen:
<Name>_n.png
n = Anzahl der Zustaende (n>=2)
zum Beispiel: LightABS_2.png


**Hinweis: Anzeigezustaende mit LEDs**
Moechten Sie z.B. mit einer LED eine Lampe abbilden, die an und aus geschaltet werden kann, so 
verwenden Sie das LED Control im Panel Designer. 
Sie koennen jedem Zustand eine eigene Farbe zuordnen. Sowohl die Anzahl der Zustaende ist 
konfigurierbar, wie auch die Form der LED.

Beispiel 1: eine gruene LED abbilden
 LED Control:
  Zustand 0; Wert 0; Farbe: grau
  Zustand 1; Wert 1; Farbe: gruen

Beispiel 2: eine LED abbilden, die die Ampel-Farben besitzt
 LED Control:
  Zustand 0; Wert 0; Farbe: rot
  Zustand 1; Wert 1; Farbe: gelb
  Zustand 2; Wert 2; Farbe: gruen
