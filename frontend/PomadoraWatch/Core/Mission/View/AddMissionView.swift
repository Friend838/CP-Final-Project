//
//  AddMissionView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/10.
//

import SwiftUI

struct AddMissionView: View {
    @Environment(\.presentationMode) var presentationMode
    @State var isFullDay = false
    @State var name = ""
    @State var selectedDate = Date()
    @State var description = ""
    
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
                print(selectedDate)
                TodoService.shared.uploadTask(timestamp: selectedDate, name: name, description: description) {
                    DispatchQueue.main.async {
                        self.presentationMode.wrappedValue.dismiss()
                    }
                }
            } label: {
                Text("新增")
                    .fontWeight(.bold)
                    .frame(width: UIScreen.main.bounds.width - 32, height: 50)
                    .background(.blue)
                    .cornerRadius(10)
                    .foregroundColor(.white)
            }
        }
        .padding(.horizontal)
        .navigationTitle("Add Mission")
    }
}

struct AddMissionView_Previews: PreviewProvider {
    static var previews: some View {
        AddMissionView()
    }
}
