//
//  Task.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/3.
//
import Foundation

struct Task: Codable, Hashable {
    let userId: String
    let timestamp: String
    let name: String
    let description: String?
    let finishStatus: Bool
    let tomatoCount: Int
}
