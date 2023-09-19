//
//  MissionRowView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/3.
//

import SwiftUI

struct MissionRowView: View {
    @State var task: Task
    
    var body: some View {
        // deadline
        VStack {
            HStack(spacing: 12) {
                // Checkbox
                Image(systemName: task.finishStatus ? "checkmark.square" : "square")
                    .imageScale(.medium)
                    .font(.title)
                    .onTapGesture {
                        let newTask = Task(userId: task.userId,
                                           timestamp: task.timestamp,
                                           name: task.name,
                                           description: task.description,
                                           finishStatus: !task.finishStatus,
                                           tomatoCount: task.tomatoCount)
                        TodoService.shared.updateTask(originTask: task,
                                                      newTask: newTask) {
                            
                        }
                    }
                
                NavigationLink {
                    MissionDetailView(task: task)
                } label: {
                    // Main task
                    VStack(alignment: .leading) {
                        Text(task.name)
                            .font(.system(size: 24, weight: .semibold))
                            .foregroundColor(Color.theme.primaryTextColor)
                            .strikethrough(task.finishStatus)
                        Text(task.timestamp.toDateString())
                            .font(.system(size: 16, weight: .medium))
                            .foregroundColor(.red)
                    }
                    .frame(width: 200, alignment: .leading)
                    
                    // Tomato cycle
                    Text(String(task.tomatoCount))
                    Image("tomato")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 20)
                }
            }
            .padding(4)
            Divider()
        }
    }
}

struct MissionRowView_Previews: PreviewProvider {
    static var previews: some View {
        MissionRowView(task: dev.mockTask)
    }
}
