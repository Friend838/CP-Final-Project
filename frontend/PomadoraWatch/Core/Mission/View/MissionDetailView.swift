//
//  MissionDetailView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/15.
//

import SwiftUI

struct MissionDetailView: View {
    @Environment(\.presentationMode) var presentationMode
    let task: Task
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text(task.name)
                .font(.title)
            Text(task.timestamp.toDateString())
            Divider()
            Text("任務狀態")
            Text(task.finishStatus.description)
            Divider()
            Text("任務描述")
            Text(task.description ?? "")
            Spacer()
        }
        .padding(.horizontal)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItemGroup(placement: .navigationBarTrailing) {
                NavigationLink {
                    ModifyMissionView(task: task)
                } label: {
                    Image(systemName: "pencil")
                }

                Button {
                    TodoService.shared.deleteTask(task: task) {
                        presentationMode.wrappedValue.dismiss()
                    }
                } label: {
                    Image(systemName: "trash")
                }
            }
        }
    }
}

struct MissionDetailView_Previews: PreviewProvider {
    static var previews: some View {
        MissionDetailView(task: dev.mockTask)
    }
}
