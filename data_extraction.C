void data_extraction(string filename, string out){

  TFile* f = new TFile(filename.c_str());   //load in file
  ofstream myfile;
  myfile.open(out.c_str(), ios::app);       //open data file for radio data storage

  //Create Data structures for all parts needed:
  Sash::DataSet* events = (Sash::DataSet*)(f->Get("dstevents")); //event data structure 
  Sash::DataSet* run = (Sash::DataSet*)(f->Get("run"));   //Run information such as run length etc.
  run->GetEntry();

  Sash::DataSet* runquality = (Sash::DataSet*)(f->Get("runquality"));

  Sash::HESSArray* hess = run->GetHESSArray();      //Create Hess array
  Sash::RunHeader* runhead = hess->Get((Sash::RunHeader*)0);  //runheader with telescope involvement information

  myfile << runhead->GetRunNum() << "\t";

  //the loop over all the telescopes
  int ct;                                             //telescope number
  for(int i = 1; i <= 4; i++){
    ct = i;
    run->GetEntry();                                  //get run information
    Sash::Pointer<Sash::Telescope> tel(hess, ct);     //select telescope i
    if(runhead->CheckTelInRun(tel)){                  //check if telescope i is involved in run
      runquality->GetEntry();                         //get runquality info for meteo
      ParisRunQuality::TelescopeMeteoInformation* meteo = hess->Get(ct,(ParisRunQuality::TelescopeMeteoInformation*)0); //get meteo information for ct = i
      ParisRunQuality::TelescopeTrackingInformation* teltrack = hess->Get(ct,(ParisRunQuality::TelescopeTrackingInformation*)0);  //This is for Zenith and Azimuth
      Double_t radioT = meteo->GetMeanRadiometerTemperature();  //get radio temperature
      Double_t zenith = teltrack->GetZenithAngleMean();
      Double_t azimuth = teltrack->GetAzimuthAngleMean();
      myfile << radioT<< "\t" << zenith << "\t" << azimuth << "\t";
    } else {
        myfile << "nan\tnan\tnan\t";
    }
  }
  runquality->GetEntry();
  Sash::HESSArray* hess = runquality->GetHESSArray();
  ParisRunQuality::MeteoInformation* Meteo = hess->Get((ParisRunQuality::MeteoInformation*)0); //
  Double_t ambTemp = Meteo->GetMeanTemperature();
  Double_t RelHum = Meteo->GetMeanRelativeHumidity();

  events->GetEntry();
  Sash::HESSArray* hess = events->GetHESSArray(); //rerun hess array creation
  Sash::EventHeader* head = hess->Get((Sash::EventHeader*)0);   //get event header for time info
  Sash::Time time1 = head->GetTimeStamp();                      // get time stamp from event header
  Stash::Coordinate position = runhead->GetTargetPosition();        //Target Position
  double time = time1.GetTimeDouble();                          // convert from Sash::Time to double value
  myfile << Form("%f", time) << "\t" << Form("%f\t", (ambTemp)) << Form("%f", (RelHum)) << endl;                           //write the time value
  myfile.close();
}
//_______________________________File format output______________________________
//run number  CT1_radioT CT1_zenith CT1_azimuth CT2_radioT CT2_zenith CT2_azimuth CT3_radioT CT3_zenith CT3_azimuth CT4_radioT CT4_zenith CT4_azimuth TimeStamp ambientTemp RelHum
