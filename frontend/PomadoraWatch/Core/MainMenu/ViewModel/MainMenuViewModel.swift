//
//  MainMenuViewModel.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/18.
//

import Foundation

class MainMenuViewModel: NSObject, ObservableObject {
    @Published var timeText: String = "25:00"
    @Published var selectedTask: String = ""
    @Published var showSideMenu = false
    @Published var showTaskSelectionList = false
    var taskList: [Task] = []
    var isPause: Bool = false
    var isStart: Bool = false
    var remainTime: Int = 150000
    private var startTime: Int = 0
    private var timer: Timer? = nil
    
    override init() {
        super.init()
        TomatoTimingService.shared.registerSubscriptions { action in
            DispatchQueue.main.async {
                if action == "start_record" {
                    self.startTimer()
                    print(action)
                } else if action == "end_record" {
                    self.resetTimer()
                    self.sendCurrentTask(taskName: self.selectedTask)
                }
            }
        }
    }
    
    func startTimer() {
        if timer == nil {
            isPause = false
            isStart = true
            timer = Timer.scheduledTimer(timeInterval: 0.01, target: self, selector: #selector(secDiminish), userInfo: nil, repeats: true)
        } else {
            remainTime = 150000
        }
    }
    
    func pauseTimer() {
        if timer != nil {
            isPause = true
            isStart = false
            timer!.invalidate()
            timer = nil
        }
    }
    
    func resetTimer() {
        if timer != nil {
            isPause = false
            isStart = false
            timer!.invalidate()
            timer = nil
        }
        remainTime = 150000
    }
    
    @objc func secDiminish() {
        if (remainTime >= 0) {
            remainTime -= 1
        }
        let sec: Int = remainTime / 100
        DispatchQueue.main.async {
            self.timeText = String(format: "%d:%2.2d", (sec / 60), (sec % 60))
        }
    }
    
    func fetchTasksAndSet() {
        TodoService.shared.fetchTasksByNowAndReturn { tasks in
            self.taskList = tasks
            if tasks.isEmpty == false {
                self.selectedTask = tasks[0].name
            }
        }
    }
    
    func sendCurrentTask(userId: String = "8787878787", taskName: String) {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/records/sendTaskName")!
        var request = URLRequest(url: url)
        let json: [String: Any] = ["userId": userId,
                                   "taskName": taskName,
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
            print("Send current task succeed!")
        }

        task.resume()
    }
}
