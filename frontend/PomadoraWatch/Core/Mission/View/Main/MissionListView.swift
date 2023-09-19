//
//  MissionListView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/9.
//

import SwiftUI

struct MissionListView: View {
    @State var showTask: Bool = false
    let title: String
    let borderColor: Color
    let tasks: [Task]?
    
    var body: some View {
        VStack {
            Button {
                showTask.toggle()
            } label: {
                VStack(alignment: .center) {
                    ZStack(alignment: .center) {
                        Rectangle()
                            .frame(width: 360, height: 56)
                            .foregroundColor(borderColor)
                        HStack {
                            Text(title)
                            Spacer()
                            Text(String(tasks?.count ?? 0))
                            Image(systemName: showTask ? "arrowtriangle.down.fill": "arrowtriangle.down")
                        }
                        .padding(.horizontal, 30)
                        .font(.system(size: 24))
                        .frame(width: 354, height: 50, alignment: .leading)
                        .background(.white)
                        .foregroundColor(.black)
                    }
                }
            }
            if (showTask == true && tasks != nil) {
                ForEach(tasks!, id: \.self) {task in
                    MissionRowView(task: task)
                }
            }
        }
        .frame(maxWidth: 360)
        .background(.white)
    }
}

struct MissionListView_Previews: PreviewProvider {
    static var previews: some View {
        MissionListView(title: "已過期", borderColor: .red, tasks: nil)
    }
}
