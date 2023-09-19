//
//  PomadoraWatchApp.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/1.
//

import SwiftUI


class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        TomatoTimingService.shared
        print("Your code here")
        return true
    }
}

@main
struct PomadoraWatchApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        WindowGroup {
            MainMenuView()
        }
    }
}
