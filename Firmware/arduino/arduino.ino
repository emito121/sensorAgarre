#define F_CPU 16000000UL
#include <avr/io.h>      
#include <util/delay.h>  
#include <avr/interrupt.h>

void iniTimer2() //Extraído del firmware de la carrera de vehículos por EEG
{
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2  = 0;
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20);
  OCR2A = 155;
  TCCR2A |= (1 << WGM21);
  TIMSK2 |= (1 << OCIE2A); 
}

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT);
  iniTimer2(); //timer a 100 Hz
  interrupts();
}

void loop() {
}

ISR(TIMER2_COMPA_vect)
{
    byte valor = analogRead(A0);
    Serial.write(valor);
}
