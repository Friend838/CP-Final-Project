//
//  SideMenuButton.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/1.
//

import SwiftUI

struct SideMenuButton: View {
    @Binding var showSideMenu: Bool
    
    var body: some View {
        Button {
            withAnimation(.spring()) {
                showSideMenu.toggle()
            }
        } label: {
            Image(systemName: "line.3.horizontal")
                .font(.title)
                .foregroundColor(.orange)
                .padding()
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}
