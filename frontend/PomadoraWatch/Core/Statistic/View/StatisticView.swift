//
//  StatisticView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/3.
//

import SwiftUI
import Charts

struct StatisticView: View {
    let week: [String] = ["日", "一", "二", "三", "四", "五", "六"]
    @State var weekIndex: [Int] = [0, 1, 2, 3, 4, 5, 6]
    @State var weekday = 0
    @ObservedObject var statisticService = StatisticService.shared
    
    var body: some View {
        VStack(alignment: .center, spacing: 0) {
            ZStack {
                Color.yellow
                    .opacity(0.5)
                VStack(alignment: .leading) {
                    Text("專注統計")
                        .font(.system(size: 24))
                        .padding(.bottom, 5)
                    
                    HStack {
                        VStack(alignment: .leading) {
                            Text("總番茄")
                                .font(.system(size: 20))
                            Text("\(statisticService.statisticsBySec.reduce(0, +) / 1500)")
                                .font(.system(size: 24, weight: .semibold))
                        }
                        VStack(alignment: .leading) {
                            Text("總專注時長")
                                .font(.system(size: 20))
                            Text(statisticService.thisWeekTime)
                                .font(.system(size: 24, weight: .semibold))
                        }
                    }
                    
                    Chart {
                        ForEach(weekIndex, id:\.hashValue) { count in
                            BarMark(
                                x: .value("星期", week[count]),
                                y: .value("完成", (statisticService.statisticsBySec[count] / 60))
                            )
                        }
                    }
                    .frame(width: 320, height: 170)
                }
                .padding()
                .background(.white)
            }
            
            ZStack {
                Color.pink
                    .opacity(0.5)
                VStack(alignment: .leading) {
                    Text("任務統計")
                        .font(.system(size: 24))
                        .padding(.bottom, 5)
                    
                    VStack(alignment: .leading) {
                        Text("已完成任務總數")
                            .font(.system(size: 20))
                        Text(statisticService.totalMissionFinished)
                            .font(.system(size: 24, weight: .semibold))
                        }
                    
                    Chart {
                        ForEach(weekIndex, id:\.hashValue) { count in
                            LineMark(
                                x: .value("星期", week[count]),
                                y: .value("完成", statisticService.statisticByMissionCount[count])
                            )
                        }
                    }
                    .frame(width: 320, height: 170)
                }
                .padding()
                .background(.white)
            }
        }
        .padding(.top, 1)
        .navigationTitle("Statistic")
        .navigationBarTitleDisplayMode(.large)
        .onAppear {
            let today = Date()
            let calendar = Calendar.current
            self.weekday = calendar.component(.weekday, from: today)
            for i in 0..<7 {
                var tmp = weekday + i
                if tmp >= 7 {
                    tmp = tmp - 7
                }
                weekIndex[i] = tmp
            }
            
            StatisticService.shared.fetchStatisticsBySec {
                print(statisticService.statisticsBySec)
            }
            
            StatisticService.shared.fetchStatisticsByMissionCount {
                
            }
        }
    }
}

struct StatisticView_Previews: PreviewProvider {
    static var previews: some View {
        StatisticView()
    }
}
