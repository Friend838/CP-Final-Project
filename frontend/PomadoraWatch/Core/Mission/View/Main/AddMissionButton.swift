//
//  AddMissionButton.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/10.
//

import SwiftUI

struct AddMissionButton: View {
    var body: some View {
        NavigationLink {
            AddMissionView()
        } label: {
            Image(systemName: "plus")
                .font(.title2)
                .foregroundColor(.black)
                .padding()
                .background(.white)
                .clipShape(Circle())
                .shadow(color: .black, radius: 6)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

struct AddMissionButton_Previews: PreviewProvider {
    static var previews: some View {
        AddMissionButton()
    }
}
