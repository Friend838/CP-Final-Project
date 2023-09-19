//
//  TomatoTimingService.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/6/7.
//

import Foundation
import AWSIoT

class TomatoTimingService: ObservableObject {
    static let shared = TomatoTimingService()
    
    init() {
        // Create AWS credentials and configuration
        let credentials = AWSCognitoCredentialsProvider(regionType:.USEast1, identityPoolId: "us-east-1:1f04e3ea-5a62-4762-a958-242b03a38464")
        let configuration = AWSServiceConfiguration(region:.USEast1, credentialsProvider: credentials)
        
        // Initialising AWS IoT And IoT DataManager
        AWSIoT.register(with: configuration!, forKey: "kAWSIoT")  // Same configuration var as above
        let iotEndPoint = AWSEndpoint(urlString: "wss://a1io7cze9x1oli-ats.iot.us-east-1.amazonaws.com/mqtt") // Access from AWS IoT Core --> Settings
        let iotDataConfiguration = AWSServiceConfiguration(region: .USEast1,     // Use AWS typedef .Region
                                                           endpoint: iotEndPoint,
                                                           credentialsProvider: credentials)  // credentials is the same var as created above
            
        AWSIoTDataManager.register(with: iotDataConfiguration!, forKey: "kDataManager")

        // Access the AWSDataManager instance as follows:
        let dataManager = AWSIoTDataManager(forKey: "kDataManager")
        let group = DispatchGroup()
        group.enter()
        getAWSClientID { clientId, error in
            self.connectToAWSIoT(clientId: clientId) {
                //self.registerSubscriptions() {_ in
                group.leave()
                //}
            }
        }
        group.wait()
    }
    
    func getAWSClientID(completion: @escaping (_ clientId: String?,_ error: Error? ) -> Void) {
            // Depending on your scope you may still have access to the original credentials var
        let credentials = AWSCognitoCredentialsProvider(regionType:.EUWest1, identityPoolId: "us-east-1:1f04e3ea-5a62-4762-a958-242b03a38464")
        
        credentials.getIdentityId().continueWith(block: { (task:AWSTask<NSString>) -> Any? in
            if let error = task.error as NSError? {
                print("Failed to get client ID => \(error)")
                completion(nil, error)
                return nil  // Required by AWSTask closure
            }
        
            let clientId = task.result! as String
            print("Got client ID => \(clientId)")
            completion(clientId, nil)
            return nil // Required by AWSTask closure
        })
    }
    
    func connectToAWSIoT(clientId: String!, completion: @escaping () -> ()) {
        func mqttEventCallback(_ status: AWSIoTMQTTStatus ) {
            switch status {
            case .connecting: print("Connecting to AWS IoT")
            case .connected:
                print("Connected to AWS IoT")
                completion()
                // Register subscriptions here
                // Publish a boot message if required
            case .connectionError: print("AWS IoT connection error")
            case .connectionRefused: print("AWS IoT connection refused")
            case .protocolError: print("AWS IoT protocol error")
            case .disconnected: print("AWS IoT disconnected")
            case .unknown: print("AWS IoT unknown state")
            default: print("Error - unknown MQTT state")
            }
        }
        
        // Ensure connection gets performed background thread (so as not to block the UI)
        DispatchQueue.global(qos: .background).async {
            do {
                print("Attempting to connect to IoT device gateway with ID = \(clientId)")
                let dataManager = AWSIoTDataManager(forKey: "kDataManager")
                dataManager.connectUsingWebSocket(withClientId: "us-east-1:1f04e3ea-5a62-4762-a958-242b03a38464",
                                                    cleanSession: true,
                                                    statusCallback: mqttEventCallback)
            } catch {
                print("Error, failed to connect to device gateway => \(error)")
            }
        }
    }
    
    func registerSubscriptions(completion: @escaping (String) -> ()) {
            func messageReceived(payload: Data) {
                let payloadDictionary = jsonDataToDict(jsonData: payload)
                print("Message received: \(payloadDictionary)")
                completion(payloadDictionary["action"] as! String)
                // Handle message event here...
            }
            
            let topicArray = ["team16/phone"]
            let dataManager = AWSIoTDataManager(forKey: "kDataManager")
            
            for topic in topicArray {
                print("Registering subscription to => \(topic)")
                dataManager.subscribe(toTopic: topic,
                                      qoS: .messageDeliveryAttemptedAtLeastOnce,  // Set according to use case
                                      messageCallback: messageReceived)
            }
    }

    func publishMessage(message: String!, topic: String!) {
      let dataManager = AWSIoTDataManager(forKey: "kDataManager")
      dataManager.publishString(message, onTopic: topic, qoS: .messageDeliveryAttemptedAtLeastOnce) // Set QoS as needed
    }
    
    func jsonDataToDict(jsonData: Data?) -> Dictionary <String, Any> {
            // Converts data to dictionary or nil if error
            do {
                let jsonDict = try JSONSerialization.jsonObject(with: jsonData!, options: [])
                let convertedDict = jsonDict as! [String: Any]
                return convertedDict
            } catch {
                // Couldn't get JSON
                print(error.localizedDescription)
                return [:]
            }
    }
    
    func startActiveCountdown() {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/records/activate")!
        
        var request = URLRequest(url: url)
        let json: [String: Any] = ["userId": "8787878787",
                                   "name": "Not decided",
                                   ]
        let jsonData = try? JSONSerialization.data(withJSONObject: json)
        // create post request
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data,
                  let response = response as? HTTPURLResponse,
                  error == nil else {
                print("error", error ?? URLError(.badServerResponse))
                return
            }
            
            guard (200 ... 299) ~= response.statusCode else {                    // check for http errors
                print("statusCode should be 2xx, but is \(response.statusCode)")
                print("response = \(response)")
                return
            }
            print("Upload data succeed")
        }

        task.resume()
    }
}
