/* Socket variables */
string   address = "192.168.1.3";
int      port = 8888;
int      socket;                 // Socket handle
int      MAX_BUFF_LEN = 1024;    // Max size for reading in the buffer

// creons des int pour les signaux
int signal;
int   signal_m1;
int   signal_m5;
int   signal_m15;

input int SmallMovingAverage_M1 = 5;
input int BigMovingAverage_M1 = 32;
  
int CheckEntry_MA_M1()
  {
  
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
      if (SmallMovingAverageArray_M1[2] > SmallMovingAverageArray_M1[1]){
         
         // sell
         signal=1;
        
         }else{
         signal=3;
         }        
      }
      
   // si BigMovingAverage < SmallMovingAverage
   if (BigMovingAverageArray_M1[1] < SmallMovingAverageArray_M1[1]){
       if (SmallMovingAverageArray_M1[2] < SmallMovingAverageArray_M1[1]){
         
         // buy
         signal=0;
         
         }else{
         signal=2;
         } 
      }
   
    return signal;
  }

// Pour M5
int CheckEntry_MA_M5()
  {

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
      
         signal=1;
         
      }
      
   // si BigMovingAverage < SmallMovingAverage
   if (BigMovingAverageArray_M5[1] < SmallMovingAverageArray_M5[1]){

         signal=0;

      }
   
    return signal;
  }

// Pour M15

int CheckEntry_MA_M15()
  {

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
      
         signal=1;
         
      }
      
   // si BigMovingAverage < SmallMovingAverage
   if (BigMovingAverageArray_M15[1] < SmallMovingAverageArray_M15[1]){

         signal=0;

      }
   
    return signal;
  }

void OnInit() {

   
}


void OnDeinit(const int reason) {
   /* Closing the socket */
   // Creating the message
   char req[];
   
   Print("[INFO]\tClosing the socket.");
   
   int len = StringToCharArray("END CONNECTION\0", req)-1;
   SocketSend(socket, req, len);
   SocketClose(socket);
}


void OnTick() {
   
   // Initializing the socket
   socket = SocketCreate();
   if (socket == INVALID_HANDLE) Print("Error - 1: SocketCreate failure. ", GetLastError());
   else {
      if (SocketConnect(socket, address, port, 10000)) Print("[INFO]\tConnection stablished");
      else Print("Error - 2: SocketConnect failure. ", GetLastError());
   }
   
   // Loading the macd values
   //CopyBuffer(macd_h, MAIN_LINE, 0, 3, macd);
   //CopyBuffer(macd_h, SIGNAL_LINE, 0, 3, signal);
   
   // Charger le signal venant de Check_MA_Crossover
   signal_m1 = CheckEntry_MA_M1();
   signal_m5 = CheckEntry_MA_M5();
   signal_m15 = CheckEntry_MA_M15();
   // Sending MACD data
   Print("[INFO]\t Envoie de signal MA crossover");
   string msg;
   StringConcatenate(msg, signal_m1, ",",signal_m5, ",", signal_m15);
   
   char req[];
   int len = StringToCharArray(msg, req)-1;
   SocketSend(socket, req, len);
}

