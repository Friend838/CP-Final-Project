//
//  StatisticService.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/31.
//

import Foundation

struct TotalFocusTimeByDay: Codable {
    let Monday: Int
    let Tuesday: Int
    let Wednesday: Int
    let Thursday: Int
    let Friday: Int
    let Saturday: Int
    let Sunday: Int
}

class StatisticResponse: Codable {
    let body: TotalFocusTimeByDay
}

class StatisticByFinishedMissionCountResponse: Codable {
    let body: [TotalFocusTimeByDay]
}

class StatisticService: ObservableObject {
    static let shared = StatisticService()
    @Published var statisticsBySec: [Int] = [0, 0, 0, 0, 0, 0, 0]
    @Published var statisticByMissionCount: [Int] = [0, 0, 0, 0, 0, 0, 0]
    @Published var thisWeekTime: String = ""
    @Published var totalMissionFinished: String = ""
    
    func fetchStatisticsBySec(completion: @escaping () -> ()) {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/records/statistics?userId=8787878787")!
        
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            
            if let data = data {
                let decoder = JSONDecoder()
                do {
                    let todo = try decoder.decode(StatisticResponse.self, from: data)
                    DispatchQueue.main.async {
                        var tmp: [Int] = []
                        tmp.append(todo.body.Sunday)
                        tmp.append(todo.body.Monday)
                        tmp.append(todo.body.Tuesday)
                        tmp.append(todo.body.Wednesday)
                        tmp.append(todo.body.Thursday)
                        tmp.append(todo.body.Friday)
                        tmp.append(todo.body.Saturday)
                        self.statisticsBySec = tmp
                        
                        var sum: Int = 0
                        for i in tmp {
                            sum += i
                        }
                        let hr = sum / 3600
                        let min = (sum - hr * 3600) / 60
                        self.thisWeekTime = String(hr) + " hr " + String(min) + " min"
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
    
    func fetchStatisticsByMissionCount(completion: @escaping () -> ()) {
        let url = URL(string: "https://3cunhp8c47.execute-api.us-east-1.amazonaws.com/Prod/todos/queryFinish?userId=8787878787")!
        
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            
            if let data = data {
                let decoder = JSONDecoder()
                do {
                    let todo = try decoder.decode(StatisticByFinishedMissionCountResponse.self, from: data)
                    DispatchQueue.main.async {
                        print(todo.body)
                        
                        var tmp: [Int] = []
                        tmp.append(todo.body[0].Sunday)
                        tmp.append(todo.body[0].Monday)
                        tmp.append(todo.body[0].Tuesday)
                        tmp.append(todo.body[0].Wednesday)
                        tmp.append(todo.body[0].Thursday)
                        tmp.append(todo.body[0].Friday)
                        tmp.append(todo.body[0].Saturday)
                        self.statisticByMissionCount = tmp
                        
                        var sum: Int = 0
                        for i in tmp {
                            sum += i
                        }
                        self.totalMissionFinished = String(sum)
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
}
