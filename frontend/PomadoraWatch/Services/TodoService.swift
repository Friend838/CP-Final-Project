//
//  TaskServices.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/10.
//

import Foundation

class TodoResponse: Codable {
    let body: [Task]
}
class TodoService: ObservableObject {
    static let shared = TodoService()
    @Published var userTask: [Task]?
    
    func fetchTasks() {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/todos/query?userId=8787878787&start_timestamp=1583475200&end_timestamp=1783561600")!

        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            
            if let data = data {
                let decoder = JSONDecoder()
                do {
                    let todo = try decoder.decode(TodoResponse.self, from: data)
                    DispatchQueue.main.async {
                        self.userTask = todo.body
                        print(todo.body)
                    }
                } catch {
                    print(error)
                }
            } else if let error = error {
                print("HTTP Request Failed \(error)")
            }
        }

        task.resume()
    }
    
    func fetchTasksByNowAndReturn(completion: @escaping ([Task]) -> ()) {
        let now = String(Date().timeIntervalSince1970)
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/todos/query?userId=8787878787&start_timestamp=\(now)&end_timestamp=1783561600")!

        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            
            if let data = data {
                let decoder = JSONDecoder()
                do {
                    let todo = try decoder.decode(TodoResponse.self, from: data)
                    DispatchQueue.main.async {
                        completion(todo.body)
                        print(todo.body)
                    }
                } catch {
                    print(error)
                }
            } else if let error = error {
                print("HTTP Request Failed \(error)")
            }
        }

        task.resume()
    }
    
    func uploadTask(userId: String = "8787878787", timestamp: Date, name: String, description: String, completion: @escaping () -> ()) {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/todos/insert")!
        var request = URLRequest(url: url)
        let json: [String: Any] = ["userId": userId,
                                   "timestamp": String(Int(timestamp.timeIntervalSince1970)),
                                   "name": name,
                                   "description": description
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
            completion()
            self.fetchTasks()
        }

        task.resume()
    }
    
    func updateTask(userId: String = "8787878787", originTask: Task, newTask: Task, completionHandler: @escaping () -> ()) {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/todos/update")!
        var request = URLRequest(url: url)
        var changeJson: [[String: Any]] = []
        
        if originTask.timestamp != newTask.timestamp {
            changeJson.append(["type": "todo_timestamp",
                               "content": newTask.timestamp
                              ])
        }
        if originTask.name != newTask.name {
            changeJson.append(["type": "todo_name",
                               "content": newTask.name
                              ])
        }
        if originTask.description != newTask.description {
            if let newDescription = newTask.description {
                changeJson.append(["type": "todo_description",
                                   "content": newDescription
                                  ])
            }
        }
        
        if originTask.finishStatus != newTask.finishStatus {
            changeJson.append(["type": "todo_finished",
                               "content": newTask.finishStatus
                              ])
        }
        
        let json: [String: Any] = ["userId": userId,
                                   "timestamp": originTask.timestamp,
                                   "name": originTask.name ,
                                   "attributes": changeJson
                                    ]
        let jsonData = try? JSONSerialization.data(withJSONObject: json)
        if let JSONString = String(data: jsonData!, encoding: String.Encoding.utf8) {
           print(JSONString)
        }
        
        // create post request
        request.httpMethod = "POST"
        request.httpBody = jsonData
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let _ = data,
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
            print("Update data succeed")
            DispatchQueue.main.async {
                completionHandler()
            }
            self.fetchTasks()
        }

        task.resume()
    }
    
    func deleteTask(task: Task, completionHandler: @escaping () -> ()) {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/todos/delete")!
        var request = URLRequest(url: url)
        let json: [String: Any] = ["userId": task.userId,
                                   "timestamp": task.timestamp,
                                   "name": task.name,
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
            print("Delete data succeed")
            DispatchQueue.main.async {
                completionHandler()
            }
            self.fetchTasks()
        }

        task.resume()
    }
    
    func getTasksIsExpired() -> [Task]? {
        if let userTask = userTask {
            var data: [Task]? = []
            for todo in userTask {
                if let deadline = Double(todo.timestamp) {
                    if deadline < Date().timeIntervalSince1970 {
                        data?.append(todo)
                    }
                }
            }
            return data
        }
        return nil
    }
    
    func getTasksIsToday() -> [Task]? {
        if let userTask = userTask {
            var data: [Task]? = []
            for todo in userTask {
                if let deadline = Double(todo.timestamp) {
                    if deadline > Date().timeIntervalSince1970 &&
                       deadline < Date().ceil(precision: 86400).timeIntervalSince1970 {
                        data?.append(todo)
                    }
                }
            }
            return data
        }
        return nil
    }
    
    func getTasksIsTomorrow() -> [Task]? {
        if let userTask = userTask {
            var data: [Task]? = []
            for todo in userTask {
                if let deadline = Double(todo.timestamp) {
                    if deadline > Date().ceil(precision: 86400).timeIntervalSince1970 &&
                       deadline < (Date().ceil(precision: 86400).timeIntervalSince1970 + 86400) {
                        data?.append(todo)
                    }
                }
            }
            return data
        }
        return nil
    }
    
    func getTasksIsThisWeek() -> [Task]? {
        if let userTask = userTask {
            var data: [Task]? = []
            for todo in userTask {
                if let deadline = Double(todo.timestamp) {
                    if deadline > Date().floor(precision: 604800).timeIntervalSince1970 &&
                       deadline < Date().ceil(precision: 604800).timeIntervalSince1970 {
                        data?.append(todo)
                    }
                }
            }
            return data
        }
        return nil
    }
    
    
    func getTasksNoDate() -> [Task]? {
        if let userTask = userTask {
            var data: [Task]? = []
            for todo in userTask {
                if todo.timestamp == nil {
                    data?.append(todo)
                }
            }
            return data
        }
        return nil
    }
}
