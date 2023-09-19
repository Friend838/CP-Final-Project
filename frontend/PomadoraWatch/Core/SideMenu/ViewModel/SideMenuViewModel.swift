//
//  SideMenuViewModel.swift
//  PomadoraWatch
//
//  Created by hsnl on 2023/5/3.
//

import Foundation

class SideMenuViewModel {
    let quotes = [
        "“We cannot solve problems with the kind of thinking we employed when we came up with them.” — Albert Einstein",
        "“Learn as if you will live forever, live like you will die tomorrow.” — Mahatma Gandhi",
        "“Stay away from those people who try to disparage your ambitions. Small minds will always do that, but great minds will give you a feeling that you can become great too.” — Mark Twain",
        "“When you give joy to other people, you get more joy in return. You should give a good thought to happiness that you can give out.”— Eleanor Roosevelt",
        "“When you change your thoughts, remember to also change your world.” — Norman Vincent Peale",
        "“It is only when we take chances, when our lives improve. The initial and the most difficult risk that we need to take is to become honest.” — Walter Anderson",
        "“Nature has given us all the pieces required to achieve exceptional wellness and health, but has left it to us to put these pieces together.” — Diane McLaren"
    ]
    func randomQuote() -> String {
        // let randomInt = Int.random(in: 0 ..< (quotes.count - 1))
        let randomInt: Int = 1
        return quotes[randomInt]
    }
}
