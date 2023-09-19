//
//  DeveloperPreview.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/2.
//
import SwiftUI

extension PreviewProvider {
    static var dev: DeveloperPreview {
        return DeveloperPreview.shared
    }
}

class DeveloperPreview {
    static let shared = DeveloperPreview()
    
    let mockUser = User(fullname: "Bowen",
                        email: "test@gmail.com",
                        uid: NSUUID().uuidString
    )
    
    let mockTask = Task(userId: "8787878787", timestamp: "1683590400", name: "測試事件", description: "測試內容", finishStatus: false, tomatoCount: 0)
}
