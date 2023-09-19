//
//  MainMenu.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/1.
//

import SwiftUI

struct MainMenuView: View {
    let user = User(fullname: "Bowen",
                    email: "test@gmail.com",
                    uid: NSUUID().uuidString)
    @ObservedObject private var viewModel = MainMenuViewModel()
    
    var body: some View {
        NavigationStack {
            ZStack(alignment: .leading) {
                ZStack(alignment: .top) {
                    SideMenuButton(showSideMenu: $viewModel.showSideMenu)
                    
                    Rectangle()
                        .frame(height: 1)
                        .opacity(0.7)
                        .foregroundColor(Color(.orange))
                        .shadow(color: .black.opacity(0.7), radius: 4)
                        .padding(.top, 50)
                    
                    background
                    tomatoTimer
                    
                    if viewModel.showTaskSelectionList == true {
                        taskSelectionView
                            .padding(.top, 500)
                    }
                }
                .offset(x: viewModel.showSideMenu ? 300 : 0)
                
                if viewModel.showSideMenu {
                    ZStack {
                        Color.white
                            .shadow(color: viewModel.showSideMenu ? .black : .clear,
                                    radius: 10)
                        SideMenuView(user: user)
                    }
                    .ignoresSafeArea()
                    .frame(width: 300)
                }
            }
            .onAppear {
                viewModel.showSideMenu = false
                //TodoService.shared.fetchTasks()
            }
        }
        .toolbar(.hidden)
        .onAppear {
            viewModel.fetchTasksAndSet()
        }
    }
}


extension MainMenuView {
    var background: some View {
        HStack(alignment: .top) {
            VStack {
                Image("pumpkin_right")
                    .padding(.bottom, 250)
                Image("green_pepper_right")
                    .padding(.leading, -35)
            }
            .padding(.top, 20)
            
            Spacer()

            VStack {
                Image("green_pepper_left")
                    .padding(.bottom, 250)
                    .padding(.leading, 16)
                Image("pumpkin_left")
                    .padding(.leading, 5)
            }
        }
        .padding(.top, 50)
    }
    
    var tomatoTimer: some View {
        VStack(alignment: .center) {
            ZStack(alignment: .top) {
                Image("tomato")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 300)
                Text(viewModel.timeText)
                    .font(.system(size: 60, weight: .semibold))
                    .foregroundColor(.white)
                    .shadow(color: .black, radius: 2)
                    .padding(.top, 140)
            }
            .padding(.top, 200)
            
            Button {
                viewModel.showTaskSelectionList.toggle()
            } label: {
                Text("任務： \(viewModel.selectedTask)")
                    .font(.system(size: 24, weight: .semibold))
                    .padding(.top)
                    .foregroundColor(.black)
            }
            
            Button {
                TomatoTimingService.shared.startActiveCountdown()
                /*
                if viewModel.isStart == false {
                    viewModel.startTimer()
                    
                } else {
                    viewModel.pauseTimer()
                }
                print(viewModel.timeText)
                 */
            } label: {
                Ellipse()
                    .foregroundColor(.cyan)
                    .opacity(0.7)
                    .overlay {
                        Text("主動計時")
                            .foregroundColor(.black)
                    }
                    .frame(width: 150, height: 60)
                    .padding(.top, 10)
            }
        }
    }
    
    var taskSelectionView: some View {
        ZStack(alignment: .top) {
            RoundedRectangle(cornerRadius: 10)
                .foregroundColor(.white)
            
            VStack(alignment: .center) {
                Text("請選擇現在要做的事")
                    .font(.system(.title2))
                    .fontWeight(.bold)
                
                Divider()
                List {
                    ForEach(viewModel.taskList, id: \.self) { task in
                        Text(task.name)
                            .font(.system(.headline))
                            .onTapGesture {
                                viewModel.selectedTask = task.name
                                viewModel.showTaskSelectionList = false
                            }
                    }
                }
                .scrollContentBackground(.hidden)
            }
            .padding(.top)
        }
        .frame(height: 250)
    }
}


struct MainMenuView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationStack {
            MainMenuView()
        }
    }
}
