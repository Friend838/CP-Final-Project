//
//  SideMenuView.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/2.
//

import SwiftUI

struct SideMenuView: View {
    let viewModel: SideMenuViewModel = SideMenuViewModel()
    private let user: User
    
    init(user: User) {
        self.user = user
    }
    
    var body: some View {
        VStack(spacing: 40) {
            // header view
            VStack(alignment: .leading, spacing: 32) {
                // user info
                HStack {
                    Image("handsome_guy")
                        .resizable()
                        .scaledToFill()
                        .clipShape(Circle())
                        .frame(width: 64, height: 64)
                    
                    VStack(alignment: .leading, spacing: 8) {
                        Text(user.fullname)
                            .font(.system(size: 16, weight: .semibold))
                        
                        Text(user.email)
                            .font(.system(size: 14))
                            .accentColor(Color.theme.primaryTextColor)
                            .opacity(0.77)
                    }
                }
                
                // become a driver ad
                VStack(alignment: .leading, spacing: 6) {
                    Text("Random quote:")
                        .font(.footnote)
                        .fontWeight(.semibold)
                    
                    HStack {
                        Text(viewModel.randomQuote())
                            .font(.system(size: 16, weight: .semibold))
                            .padding(.trailing)
                    }
                }
                
                Rectangle()
                    .frame(width: 268, height: 1)
                    .opacity(0.7)
                    .foregroundColor(Color(.separator))
                    .shadow(color: .black.opacity(0.7), radius: 4)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.leading, 16)
            
            // option list
            VStack {
                ForEach(SideMenuOptionViewModel.allCases) { viewModel in
                    NavigationLink(value: viewModel) {
                        SideMenuOptionView(viewModel: viewModel)
                            .padding()
                    }
                }
            }
            .navigationDestination(for: SideMenuOptionViewModel.self) { viewModel in
                switch viewModel {
                case .mission:
                    MissionView()
                case .statistic:
                    StatisticView()
                case .settings:
                    SettingsView(user: user)
                }
                
            }
            Spacer()
            Text("Pomadora clock v0.0.1")
                .font(.system(size: 12, weight: .light))
                .padding(.bottom, 32)
        }
        .frame(width: 300)
        .padding(.top, 60)
    }
}

struct SideMenuView_Previews: PreviewProvider {
    static var previews: some View {
        SideMenuView(user: dev.mockUser)
    }
}
