#define F_CPU 16000000UL // Defining the CPU Frequency

//#define FREC_INTERRUPT  100000 //en Hz
//#define PRE_SCALER      1UL

#include <avr/io.h>      // Contains all the I/O Register Macros
#include <util/delay.h>  // Generates a Blocking Delay
#include <avr/interrupt.h> // Contains all interrupt vectors

void iniTimer2()
{
  TCCR2A = 0;// pongo a cero el registro de control del timer2 (pagina 155)
  TCCR2B = 0;// idem para TCCR2B
  TCNT2  = 0;//valor inicial del contador en 0
  // Seteo el preescaler en 1
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20);
  //seteamos el timer2 para interrupción cada 1ms, que es el máximo tiempo que podemos alcanzar
  OCR2A = 155; // = (16MHz/(preScaler*frecuencia de Interrupción))-1
  //Modo Contador (Clear Timer on Compare Match (CTC))
  TCCR2A |= (1 << WGM21);

  // Habilito la comparación
  TIMSK2 |= (1 << OCIE2A);    //ver pagina 160
}

void setup() {
  Serial.begin(9600);//iniciailzamos la comunicación
  pinMode(A0, INPUT);
  iniTimer2(); //inicio timer 2
  interrupts();//Habilito las interrupciones
}

void loop() {
}

ISR(TIMER2_COMPA_vect)//Rutina interrupción Timer1, configurado a 10ms
{
  int valor = analogRead(A0)
  Serial.write(valor);
  }
}
