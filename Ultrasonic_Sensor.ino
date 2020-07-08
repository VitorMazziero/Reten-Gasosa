const int pingPin = 7; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 6; // Echo Pin of Ultrasonic Sensor
char userImput;

void setup() {
    Serial.begin(9600); // reenable serial again
    pinMode(13, OUTPUT);
}


void loop() {
    long duration, mm;
    pinMode(pingPin, OUTPUT);
    digitalWrite(pingPin, LOW);
    delayMicroseconds(2);
    digitalWrite(pingPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(pingPin, LOW);
    pinMode(echoPin, INPUT);
    duration = pulseIn(echoPin, HIGH);;
    mm = microsecondsToCentimeters(duration);
    Serial.print(mm);
    Serial.println();
    digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(500);
}
long microsecondsToCentimeters(long microseconds) {
   return microseconds/2.9/2;
}
