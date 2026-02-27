package 'Complex Drone System' {
   // Import standard libraries
   private import ScalarValues::*;
   private import ISQ::*;

   // Requirements Package
   package Requirements {
      requirement def PerformanceRequirement {
         doc /* Base requirement for performance specifications */
         attribute description : String;
      }

      requirement def SafetyRequirement {
         doc /* Base requirement for safety specifications */
         attribute description : String;
         attribute priority : String;
      }

      requirement TopLevelRequirements {
         doc /* Top-level drone system requirements */

         requirement RangeReq : PerformanceRequirement {
            doc /* Minimum range requirement */
            attribute description = "The drone shall achieve a range of at least 1500 nm";
            attribute targetValue : Real = 1500.0;
            attribute unit = "nm";
         }

         requirement MaxStructureWeight : PerformanceRequirement {
            doc /* Maximum structure weight constraint (MTOW 400 lb minus 125 lb payload) */
            attribute description = "The drone structure weight shall not exceed 325 lb";
            attribute maxValue : Real = 325.0;
            attribute unit = "lb";
         }

         requirement CruiseSpeed : PerformanceRequirement {
            doc /* Cruise speed for efficient long-range flight */
            attribute description = "The drone shall achieve a cruise speed of at least 100 knots";
            attribute minValue : Real = 100.0;
            attribute unit = "knots";
         }

         requirement PayloadCapacity : PerformanceRequirement {
            doc /* Payload carrying capacity */
            attribute description = "The drone shall carry a payload of at least 125 lb";
            attribute minValue : Real = 125.0;
            attribute unit = "lb";
         }

         requirement OperatingTemperature : PerformanceRequirement {
            doc /* Operating temperature range */
            attribute description = "The drone shall operate in temperatures from -10°C to 45°C";
            attribute minTemp : Real = -10.0;
            attribute maxTemp : Real = 45.0;
            attribute unit = "°C";
         }

         requirement FailSafeReq : SafetyRequirement {
            doc /* Fail-safe system requirement */
            attribute description = "The drone shall return to home on signal loss";
            attribute priority = "Critical";
         }

         requirement BatteryMonitoring : SafetyRequirement {
            doc /* Battery monitoring requirement */
            attribute description = "The system shall monitor battery voltage and initiate landing at 15% capacity";
            attribute priority = "Critical";
         }

         requirement PositionAccuracy : PerformanceRequirement {
            doc /* GPS position accuracy */
            attribute description = "The drone shall maintain position accuracy within 2.5m";
            attribute maxError : Real = 2.5;
            attribute unit = "m";
         }

         requirement VideoTransmissionRange : PerformanceRequirement {
            doc /* Video transmission range requirement */
            attribute description = "Video transmission shall work up to 1000m range";
            attribute minRange : Real = 1000.0;
            attribute unit = "m";
         }

         requirement ControlRange : PerformanceRequirement {
            doc /* Control signal range requirement */
            attribute description = "Control signals shall work up to 1500m range";
            attribute minRange : Real = 1500.0;
            attribute unit = "m";
         }
      }
   }

   // Part Definitions with Attributes
   part def HeavyFuelEngine {
      doc /* Heavy fuel internal combustion engine for propulsion */
      attribute displacement : Real;  // cubic centimeters
      attribute maxPower : Real;  // horsepower
      attribute maxRPM : Real;  // revolutions per minute
      attribute mass : Real;  // lb
      attribute fuelType : String;  // JP-5, JP-8, Diesel, etc.
      attribute sfc : Real;  // specific fuel consumption (lb/hp/hr)
      attribute cylinderConfig : String;
   }

   part def BrusshlessMotor {
      doc /* Brushless DC motor for propulsion */
      attribute kv : Real;  // RPM per volt
      attribute maxCurrent : Real;  // Amperes
      attribute voltage : Real;  // Volts
      attribute mass : Real;  // kg
      attribute maxPower : Real;  // Watts
      attribute efficiency : Real;  // percentage

      assert constraint PowerConstraint {
         maxPower == voltage * maxCurrent
      }
   }

   part def ESC {
      doc /* Electronic Speed Controller */
      attribute maxCurrent : Real;  // Amperes
      attribute voltage : Real;  // Volts
      attribute mass : Real;  // kg
      attribute refreshRate : Real;  // Hz
      attribute protocol : String;
   }

   part def Propeller {
      doc /* Propeller for thrust generation */
      attribute diameter : Real;  // inches
      attribute pitch : Real;  // inches
      attribute mass : Real;  // kg
      attribute maxThrust : Real;  // Newtons
      attribute material : String;
   }

   part def LiPoBattery {
      doc /* Lithium Polymer battery */
      attribute capacity : Real;  // mAh
      attribute voltage : Real;  // Volts
      attribute cellCount : Integer;
      attribute mass : Real;  // kg
      attribute dischargeRate : Real;  // C rating
      attribute maxContinuousCurrent : Real;  // Amperes

      assert constraint VoltageConstraint {
         voltage == cellCount * 3.7
      }

      assert constraint CurrentConstraint {
         maxContinuousCurrent == capacity * dischargeRate / 1000.0
      }
   }

   part def FlightController {
      doc /* Main flight control computer */
      attribute processor : String;
      attribute clockSpeed : Real;  // MHz
      attribute mass : Real;  // kg
      attribute voltage : Real;  // Volts
      attribute imuUpdateRate : Real;  // Hz
      attribute numberOfPorts : Integer;
      attribute firmware : String;
   }

   part def IMUSensor {
      doc /* Inertial Measurement Unit sensor */
      attribute type : String;
      attribute updateRate : Real;  // Hz
      attribute mass : Real;  // kg
      attribute accuracy : Real;
      attribute range : Real;
   }

   part def GPSModule {
      doc /* GPS receiver module */
      attribute type : String;
      attribute updateRate : Real;  // Hz
      attribute accuracy : Real;  // meters
      attribute channels : Integer;
      attribute mass : Real;  // kg
      attribute voltage : Real;  // Volts
   }

   part def Camera {
      doc /* Video camera for payload */
      attribute resolution : String;
      attribute frameRate : Real;  // fps
      attribute mass : Real;  // kg
      attribute fov : Real;  // degrees
      attribute sensor : String;
      attribute voltage : Real;  // Volts
      attribute powerConsumption : Real;  // Watts
   }

   part def Gimbal {
      doc /* Camera stabilization gimbal */
      attribute axes : Integer;
      attribute mass : Real;  // kg
      attribute maxPayload : Real;  // kg
      attribute stabilizationAccuracy : Real;  // degrees
      attribute material : String;
   }

   part def RadioReceiver {
      doc /* RC radio receiver */
      attribute frequency : Real;  // GHz
      attribute channels : Integer;
      attribute protocol : String;
      attribute range : Real;  // meters
      attribute mass : Real;  // kg
      attribute voltage : Real;  // Volts
   }

   part def TelemetryModule {
      doc /* Bidirectional telemetry transceiver */
      attribute frequency : Real;  // GHz
      attribute dataRate : Real;  // kbps
      attribute range : Real;  // meters
      attribute mass : Real;  // kg
      attribute voltage : Real;  // Volts
      attribute powerOutput : Real;  // mW
   }

   part def VideoTransmitter {
      doc /* Video transmission system */
      attribute frequency : Real;  // GHz
      attribute channels : Integer;
      attribute powerOutput : Real;  // mW
      attribute range : Real;  // meters
      attribute mass : Real;  // kg
      attribute voltage : Real;  // Volts
   }

   part def Frame {
      doc /* Main structural frame */
      attribute material : String;
      attribute armLength : Real;  // mm
      attribute mass : Real;  // kg
      attribute motorMountSpacing : Real;  // mm
      attribute maxPayloadCapacity : Real;  // kg
   }

   // Main Drone System
   part Drone {
      doc /* Group 3 expendable tailless flying wing UAV system assembly */

      attribute totalMass : Real;  // lb
      attribute maxRange : Real;  // nm
      attribute cruiseSpeed : Real;  // knots
      attribute maxAltitude : Real;  // feet
      attribute uavClass : String = "Group 3";  // US DoD UAS classification
      attribute configuration : String = "Tailless flying wing";

      // System-level constraints
      assert constraint MassConstraint {
         totalMass <= 275.0
      }

      // Requirement satisfaction
      satisfy Requirements::TopLevelRequirements::MaxStructureWeight by Drone;
      satisfy Requirements::TopLevelRequirements::RangeReq by 'Power System';
      satisfy Requirements::TopLevelRequirements::CruiseSpeed by 'Propulsion System';

      part 'Propulsion System' {
         doc /* Heavy fuel propulsion system for long-range fixed-wing UAV */

         attribute totalThrust : Real;  // Newtons
         attribute totalPowerOutput : Real;  // horsepower

         satisfy Requirements::TopLevelRequirements::CruiseSpeed;

         part engine : HeavyFuelEngine {
            attribute displacement = 215.0;  // cc
            attribute maxPower = 23.0;  // hp at 6500 RPM
            attribute maxRPM = 6500.0;
            attribute mass = 12.5;  // lb
            attribute fuelType = "JP-8 / Jet-A / Diesel";
            attribute sfc = 0.45;  // lb/hp/hr specific fuel consumption
            attribute cylinderConfig = "2-cylinder horizontally opposed";
         }

         part propeller : Propeller {
            attribute diameter = 32.0;  // inches
            attribute pitch = 14.0;  // inches
            attribute mass = 1.2;  // lb
            attribute maxThrust = 400.0;  // Newtons
            attribute material = "Carbon Fiber";
         }

         part fuelSystem {
            doc /* Fuel storage and delivery system */
            attribute fuelCapacity : Real = 18.0;  // gallons
            attribute fuelMass : Real = 126.0;  // lb (at 7 lb/gal for JP-8)
            attribute tankMaterial : String = "Aluminum";
            attribute tankMass : Real = 8.0;  // lb
            attribute fuelPumpType : String = "Mechanical engine-driven";
         }

         part starter {
            doc /* Engine starter system */
            attribute type : String = "Electric starter";
            attribute voltage : Real = 12.0;
            attribute mass : Real = 1.5;  // lb
         }
      }

      part 'Power System' {
         doc /* Electrical power generation and distribution for avionics */

         attribute systemVoltage : Real;  // Volts
         attribute estimatedRange : Real;  // nm

         satisfy Requirements::TopLevelRequirements::RangeReq;
         satisfy Requirements::TopLevelRequirements::BatteryMonitoring;

         part alternator {
            doc /* Engine-driven alternator for electrical power */
            attribute outputPower : Real = 500.0;  // Watts
            attribute voltage : Real = 28.0;  // 28V DC standard
            attribute mass : Real = 3.5;  // lb
            attribute efficiency : Real = 85.0;
         }

         part avionicsBattery : LiPoBattery {
            doc /* Backup battery for avionics and engine start */
            attribute capacity = 8000.0;  // mAh
            attribute voltage = 24.0;  // 6S LiPo
            attribute cellCount = 6;
            attribute mass = 4.5;  // lb
            attribute dischargeRate = 10.0;
            attribute maxContinuousCurrent = 80.0;
         }

         part powerDistributionBoard {
            doc /* Distributes power to all components */
            attribute maxCurrent : Real = 40.0;
            attribute voltage : Real = 28.0;
            attribute mass : Real = 0.6;  // lb
            attribute numberOfOutputs : Integer = 12;
         }

         part voltageRegulator5V {
            doc /* 5V regulator for avionics */
            attribute inputVoltage : Real = 28.0;
            attribute outputVoltage : Real = 5.0;
            attribute maxCurrent : Real = 10.0;
            attribute mass : Real = 0.3;  // lb
            attribute efficiency : Real = 92.0;
         }

         part voltageRegulator12V {
            doc /* 12V regulator for payload and sensors */
            attribute inputVoltage : Real = 28.0;
            attribute outputVoltage : Real = 12.0;
            attribute maxCurrent : Real = 8.0;
            attribute mass : Real = 0.4;  // lb
            attribute efficiency : Real = 90.0;
         }
      }

      part 'Flight Control System' {
         doc /* Navigation, stabilization and control for autonomous long-range flight */

         satisfy Requirements::TopLevelRequirements::FailSafeReq;
         satisfy Requirements::TopLevelRequirements::PositionAccuracy;
         satisfy Requirements::TopLevelRequirements::OperatingTemperature;

         part flightController : FlightController {
            attribute processor = "Pixhawk 6X (STM32H7)";
            attribute clockSpeed = 480.0;
            attribute mass = 0.35;  // lb
            attribute voltage = 5.0;
            attribute imuUpdateRate = 8000.0;
            attribute numberOfPorts = 16;
            attribute firmware = "ArduPlane";
         }

         part gyroscope : IMUSensor {
            attribute type = "ICM-42688";
            attribute updateRate = 8000.0;
            attribute mass = 0.01;  // lb
            attribute accuracy = 0.01;
            attribute range = 2000.0;  // degrees per second
         }

         part accelerometer : IMUSensor {
            attribute type = "ICM-42688";
            attribute updateRate = 8000.0;
            attribute mass = 0.01;  // lb
            attribute accuracy = 0.02;
            attribute range = 16.0;  // g
         }

         part magnetometer : IMUSensor {
            attribute type = "RM3100";
            attribute updateRate = 200.0;
            attribute mass = 0.02;  // lb
            attribute accuracy = 0.3;
            attribute range = 8.0;  // gauss
         }

         part barometer {
            doc /* Atmospheric pressure sensor for altitude */
            attribute type : String = "MS5611";
            attribute updateRate : Real = 100.0;
            attribute mass : Real = 0.02;  // lb
            attribute accuracy : Real = 1.0;  // meters
            attribute range : Real = 15000.0;  // meters
         }

         part gps : GPSModule {
            attribute type = "UBLOX F9P RTK";
            attribute updateRate = 10.0;
            attribute accuracy = 0.01;  // RTK accuracy in meters
            attribute channels = 184;
            attribute mass = 0.15;  // lb
            attribute voltage = 5.0;
         }

         part airspeedSensor {
            doc /* Pitot tube for airspeed measurement */
            attribute type : String = "MS4525DO";
            attribute updateRate : Real = 100.0;
            attribute mass : Real = 0.05;  // lb
            attribute accuracy : Real = 0.5;  // m/s
            attribute maxSpeed : Real = 100.0;  // m/s
         }
      }

      part 'Communication System' {
         doc /* Long-range control, telemetry and data transmission */

         satisfy Requirements::TopLevelRequirements::VideoTransmissionRange;
         satisfy Requirements::TopLevelRequirements::ControlRange;

         part radioReceiver : RadioReceiver {
            attribute frequency = 0.433;  // GHz (433 MHz for long range)
            attribute channels = 16;
            attribute protocol = "RFD900x";
            attribute range = 60000.0;  // meters (~32 nm)
            attribute mass = 0.25;  // lb
            attribute voltage = 5.0;
         }

         part telemetryModule : TelemetryModule {
            attribute frequency = 0.900;  // GHz (900 MHz band)
            attribute dataRate = 250.0;  // kbps
            attribute range = 80000.0;  // meters (~43 nm)
            attribute mass = 0.3;  // lb
            attribute voltage = 5.0;
            attribute powerOutput = 1000.0;  // mW (1W)
         }

         part satelliteComm {
            doc /* Iridium satellite transceiver for beyond-line-of-sight */
            attribute type : String = "Iridium 9603";
            attribute dataRate : Real = 2.4;  // kbps
            attribute range : Real = 999999.0;  // Global coverage
            attribute mass : Real = 0.4;  // lb
            attribute voltage : Real = 5.0;
            attribute powerConsumption : Real = 1.4;  // Watts average
         }

         part videoTransmitter : VideoTransmitter {
            attribute frequency = 1.3;  // GHz (L-band for long range)
            attribute channels = 8;
            attribute powerOutput = 2000.0;  // mW (2W)
            attribute range = 50000.0;  // meters (~27 nm)
            attribute mass = 0.6;  // lb
            attribute voltage = 12.0;
         }
      }

      part 'Payload System' {
         doc /* Mission payload and sensor systems - up to 100 lb capacity */

         satisfy Requirements::TopLevelRequirements::PayloadCapacity;

         part eoirCamera : Camera {
            attribute resolution = "1080p@30fps";
            attribute frameRate = 30.0;
            attribute mass = 5.0;  // lb
            attribute fov = 60.0;
            attribute sensor = "1-inch CMOS with 30x optical zoom";
            attribute voltage = 12.0;
            attribute powerConsumption = 15.0;  // Watts
         }

         part thermalCamera {
            doc /* Long-wave infrared thermal imaging */
            attribute resolution : String = "640x512";
            attribute frameRate : Real = 30.0;
            attribute mass : Real = 3.5;  // lb
            attribute fov : Real = 25.0;
            attribute sensor : String = "LWIR Uncooled VOx";
            attribute voltage : Real = 12.0;
            attribute powerConsumption : Real = 8.0;  // Watts
         }

         part gimbal : Gimbal {
            attribute axes = 3;
            attribute mass = 8.0;  // lb
            attribute maxPayload = 15.0;  // lb
            attribute stabilizationAccuracy = 0.005;
            attribute material = "Machined Aluminum";
         }

         part gimbalController {
            doc /* Gimbal stabilization controller */
            attribute processor : String = "STM32H7";
            attribute mass : Real = 0.3;  // lb
            attribute voltage : Real = 12.0;
            attribute updateRate : Real = 2000.0;  // Hz
            attribute controlAlgorithm : String = "Advanced PID with IMU fusion";
         }

         part lidarSensor {
            doc /* LiDAR for terrain mapping and obstacle avoidance */
            attribute type : String = "Velodyne Puck Lite";
            attribute range : Real = 100.0;  // meters
            attribute accuracy : Real = 0.03;  // meters
            attribute mass : Real = 1.2;  // lb
            attribute voltage : Real = 12.0;
            attribute scanRate : Real = 10.0;  // Hz
         }

         part additionalPayloadBay {
            doc /* Reserved space for mission-specific sensors/equipment */
            attribute availableCapacity : Real = 82.0;  // lb remaining
            attribute volumeCapacity : Real = 3000.0;  // cubic inches
            attribute powerAvailable : Real = 500.0;  // Watts
         }
      }

      part Airframe {
         doc /* Aluminum tailless flying wing structure - expendable design */

         part centerBody : Frame {
            doc /* Central body housing avionics, engine, and payload */
            attribute material = "Aluminum Alloy (6061-T6)";
            attribute length = 2500.0;  // mm (2.5 meters)
            attribute mass = 45.0;  // lb
            attribute width = 800.0;  // mm
            attribute maxPayloadCapacity = 100.0;  // lb
            attribute construction : String = "Semi-monocoque aluminum structure";
         }

         part wing {
            doc /* Main wing assembly with integrated control surfaces */
            attribute material : String = "Aluminum Alloy with riveted ribs";
            attribute wingspan : Real = 4500.0;  // mm (4.5 meters)
            attribute area : Real = 4.0;  // square meters (slightly larger for tailless stability)
            attribute mass : Real = 42.0;  // lb (aluminum construction)
            attribute airfoil : String = "Reflexed airfoil for tailless stability";
            attribute construction : String = "Aluminum skin with internal ribs";
         }

         part elevons {
            doc /* Combined elevator and aileron control surfaces */
            attribute material : String = "Aluminum Alloy";
            attribute mass : Real = 6.0;  // lb
            attribute numberOfSurfaces : Integer = 4;  // Two per wing
            attribute controlAuthority : String = "Pitch and roll control";
            attribute actuatorType : String = "Digital servo";
         }

         part winglets {
            doc /* Optional vertical winglets for yaw stability */
            attribute material : String = "Aluminum Alloy";
            attribute mass : Real = 3.0;  // lb
            attribute height : Real = 300.0;  // mm
            attribute cant : Real = 10.0;  // degrees outward cant
         }

         part landingGear {
            doc /* Fixed landing gear assembly - expendable design */
            attribute material : String = "Aluminum Alloy";
            attribute type : String = "Fixed tricycle";
            attribute mass : Real = 8.0;  // lb
            attribute shockAbsorption : String = "Spring steel with foam padding";
            attribute expendable : Boolean = true;
         }

         part avionicsBay {
            doc /* Aluminum avionics compartment in center body */
            attribute material : String = "Aluminum with thermal insulation";
            attribute volume : Real = 1200.0;  // cubic inches
            attribute mass : Real = 7.0;  // lb
            attribute environmentalControl : String = "Passive thermal management";
            attribute construction : String = "Welded aluminum box structure";
         }
      }
   }
}
