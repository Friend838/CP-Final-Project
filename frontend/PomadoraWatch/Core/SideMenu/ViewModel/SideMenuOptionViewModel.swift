//
//  SideMenuViewModel.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/2.
//

import Foundation

enum SideMenuOptionViewModel: Int, CaseIterable, Identifiable {
    case mission
    case statistic
    case settings
    
    var title: String {
        switch self {
        case .mission: return "Missions"
        case .statistic: return "Statistic"
        case .settings: return "Settings"
        }
    }
    
    var imageName: String {
        switch self {
        case .mission: return "list.bullet.rectangle"
        case .statistic: return "chart.bar"
        case .settings: return "gear"
        }
    }
    
    var id: Int {
        return self.rawValue
    }
}
