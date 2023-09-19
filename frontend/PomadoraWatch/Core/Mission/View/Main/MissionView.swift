//
//  MissionView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/3.
//

import SwiftUI

struct MissionView: View {
    @ObservedObject var todoservice = TodoService.shared
    
    var body: some View {
        ZStack(alignment: .bottom) {
            Color.cyan
                .opacity(0.5)
            ScrollView {
                MissionListView(title: "已過期", borderColor: .red, tasks: todoservice.getTasksIsExpired())
                MissionListView(title: "今天", borderColor: .green, tasks: todoservice.getTasksIsToday())
                MissionListView(title: "明天", borderColor: .blue, tasks: todoservice.getTasksIsTomorrow())
                MissionListView(title: "這週", borderColor: .yellow, tasks: todoservice.getTasksIsThisWeek())
                MissionListView(title: "無日期", borderColor: .purple, tasks: todoservice.getTasksNoDate())
            }
            .padding(.top)
            AddMissionButton()
                .padding(.horizontal)
                .padding(.bottom, 24)
        }
        .navigationTitle("Mission")
        .navigationBarTitleDisplayMode(.large)
        .edgesIgnoringSafeArea(.bottom)
        .onAppear {
            todoservice.fetchTasks()
        }
    }
}

struct MissionView_Previews: PreviewProvider {
    static var previews: some View {
        MissionView()
    }
}
