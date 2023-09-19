//
//  String.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/11.
//

import Foundation

extension String {
    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd  hh:mm a"
        return formatter
    }
    
    func toDateString() -> String {
        let tmp = Double(self)
        let tmpDate = Date(timeIntervalSince1970: tmp ?? 0)
        return dateFormatter.string(from: tmpDate)
    }
}
