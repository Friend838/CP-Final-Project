//
//  ModifyMissionView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/17.
//

import SwiftUI

struct ModifyMissionView: View {
    @Environment(\.presentationMode) var presentationMode
    let task: Task
    @State var isFullDay = false
    @State var name: String
    @State var selectedDate: Date
    @State var description: String
    
    init(task: Task) {
        self.task = task
        _name = State(initialValue: task.name)
        _selectedDate = State(initialValue: Date(timeIntervalSince1970: Double(task.timestamp) ?? 0))
        _description = State(initialValue: task.description ?? "")
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            TextField("新增標題", text: $name, axis: .vertical)
                .font(.title)
            Divider()
            Toggle("全天", isOn: $isFullDay)
            DatePicker("時間", selection: $selectedDate, displayedComponents: isFullDay ? .date : [.date, .hourAndMinute])
            Divider()
            Text("任務描述")
            TextField("描述", text: $description, axis: .vertical)
            Spacer()
            Button {
                print(task.name)
                print(name)
                let newTask = Task(userId: task.userId,
                                   timestamp: String(Int(selectedDate.timeIntervalSince1970)),
                                   name: name,
                                   description: description,
                                   finishStatus: task.finishStatus,
                                   tomatoCount: task.tomatoCount
                                )
                
                TodoService.shared.updateTask(originTask: task,
                                              newTask: newTask) {
                    self.presentationMode.wrappedValue.dismiss()
                }
            } label: {
                Text("修改")
                    .fontWeight(.bold)
                    .frame(width: UIScreen.main.bounds.width - 32, height: 50)
                    .background(.blue)
                    .cornerRadius(10)
                    .foregroundColor(.white)
            }
        }
        .padding(.horizontal)
        .navigationTitle("Modify mission")
    }
}

struct ModifyMissionView_Previews: PreviewProvider {
    static var previews: some View {
        ModifyMissionView(task: dev.mockTask)
    }
}
