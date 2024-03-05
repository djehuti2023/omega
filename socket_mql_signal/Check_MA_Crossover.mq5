//+------------------------------------------------------------------+
//|                                            SimpleCrossoverEA.mq5 |
//|                                                        LKOT 2023 |
//|                                                                  |
//+------------------------------------------------------------------+
#property copyright "LKOT 2023"
#property version   "1.00"

   input int SmallMovingAverage_M1 = 2;
   input int BigMovingAverage_M1 = 14;
   
int CheckEntry_MA_M1()
  {

   // creons un int pour un signal
   int signal=3;
   
   // creons un tableau pour les prix
   double SmallMovingAverageArray_M1[], BigMovingAverageArray_M1[];
   
   // Definissons les proprietes de la petite moyenne mobile
   int SmallMovingAverageDefinition_M1 = iMA(_Symbol,PERIOD_M1,SmallMovingAverage_M1,0,MODE_SMA,PRICE_CLOSE);
   
   // Definissons les proprietes de la grande moyenne mobile
   int BigMovingAverageDefinition_M1 =iMA(_Symbol,PERIOD_M1,BigMovingAverage_M1,0,MODE_SMA,PRICE_CLOSE);
   
   // L'EA Defini, Une ligne, la bougie courante, 3 bougies, enreigistrer le resultat
   CopyBuffer(SmallMovingAverageDefinition_M1,0,0,3,SmallMovingAverageArray_M1);
   CopyBuffer(BigMovingAverageDefinition_M1,0,0,3,BigMovingAverageArray_M1);
   
   // si BigMovingAverage > SmallMovingAverage
   if (BigMovingAverageArray_M1[1] > SmallMovingAverageArray_M1[1]){
      
         signal=0;
         
      }
      
   // si BigMovingAverage < SmallMovingAverage
   if (BigMovingAverageArray_M1[1] < SmallMovingAverageArray_M1[1]){

         signal=1;

      }
   
    return signal;
  }

// Pour M5
int CheckEntry_MA_M5()
  {

   // creons un int pour un signal
   int signal=3;
   
   // creons un tableau pour les prix
   double SmallMovingAverageArray_M5[], BigMovingAverageArray_M5[];
   
   // Definissons les proprietes de la petite moyenne mobile
   int SmallMovingAverageDefinition_M5 = iMA(_Symbol,PERIOD_M5,SmallMovingAverage_M1,0,MODE_SMA,PRICE_CLOSE);
   
   // Definissons les proprietes de la grande moyenne mobile
   int BigMovingAverageDefinition_M5 =iMA(_Symbol,PERIOD_M5,BigMovingAverage_M1,0,MODE_SMA,PRICE_CLOSE);
   
   // L'EA Defini, Une ligne, la bougie courante, 3 bougies, enreigistrer le resultat
   CopyBuffer(SmallMovingAverageDefinition_M5,0,0,3,SmallMovingAverageArray_M5);
   CopyBuffer(BigMovingAverageDefinition_M5,0,0,3,BigMovingAverageArray_M5);
   
   // si BigMovingAverage > SmallMovingAverage
   if (BigMovingAverageArray_M5[1] > SmallMovingAverageArray_M5[1]){
      
         signal=0;
         
      }
      
   // si BigMovingAverage < SmallMovingAverage
   if (BigMovingAverageArray_M5[1] < SmallMovingAverageArray_M5[1]){

         signal=1;

      }
   
    return signal;
  }

// Pour M15

int CheckEntry_MA_M15()
  {

   // creons un int pour un signal
   int signal=3;
   
   // creons un tableau pour les prix
   double SmallMovingAverageArray_M15[], BigMovingAverageArray_M15[];
   
   // Definissons les proprietes de la petite moyenne mobile
   int SmallMovingAverageDefinition_M15 = iMA(_Symbol,PERIOD_M15,SmallMovingAverage_M1,0,MODE_SMA,PRICE_CLOSE);
   
   // Definissons les proprietes de la grande moyenne mobile
   int BigMovingAverageDefinition_M15 =iMA(_Symbol,PERIOD_M15,BigMovingAverage_M1,0,MODE_SMA,PRICE_CLOSE);
   
   // L'EA Defini, Une ligne, la bougie courante, 3 bougies, enreigistrer le resultat
   CopyBuffer(SmallMovingAverageDefinition_M15,0,0,3,SmallMovingAverageArray_M15);
   CopyBuffer(BigMovingAverageDefinition_M15,0,0,3,BigMovingAverageArray_M15);
   
   // si BigMovingAverage > SmallMovingAverage
   if (BigMovingAverageArray_M15[1] > SmallMovingAverageArray_M15[1]){
      
         signal=0;
         
      }
      
   // si BigMovingAverage < SmallMovingAverage
   if (BigMovingAverageArray_M15[1] < SmallMovingAverageArray_M15[1]){

         signal=1;

      }
   
    return signal;
  }
