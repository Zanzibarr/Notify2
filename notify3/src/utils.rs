#![allow(dead_code)]

use std::{io::{self, Write}, process::exit};

// API

#[tokio::main]
pub async fn reqget<T:std::fmt::Display>(url : T) -> Result<Option<reqwest::StatusCode>, reqwest::Error> {

    let client = reqwest::Client::new();
    let response = client.get(format!("{url}")).send().await?;
    let status_code = response.status();
    Ok(Some(status_code))

}

#[tokio::main]
pub async fn reqpost<T:std::fmt::Display>(url: T) -> Result<Option<reqwest::StatusCode>, reqwest::Error> {

    let client = reqwest::Client::new();
    let response = client.post(format!("{url}")).send().await?;
    todo!("Finish: see notify.py __request_format");
    let status_code = response.status();
    Ok(Some(status_code))

}

// LOGGING

static INFO  : &str = "\x1b[92m\x1b[1m[ INFO  ]:\x1b[0m ";
static INPUT : &str = "\x1b[94m\x1b[1m[ INPUT ]:\x1b[0m ";
static WARN  : &str = "\x1b[93m\x1b[1m[ WARN  ]:\x1b[0m ";
static ERROR : &str = "\x1b[91m\x1b[1m[ ERROR ]:\x1b[0m ";

pub fn info<T:std::fmt::Display>(msg : T) {
    eprintln!("{INFO}{msg}");
}

pub fn warn<T:std::fmt::Display>(msg: T) {
    eprintln!("{WARN}{msg}");
}

pub fn error<T:std::fmt::Display>(msg: T) {
    eprintln!("{ERROR}{msg}");
    exit(1);
}

pub fn input<T:std::fmt::Display>(
    msg : T,
    choices : &[&str]
) -> String {

    loop {

        print!("{INPUT}{msg} {choices:?} : ");
        io::stdout().flush()
            .expect("Error flushing stdout");
    
        let mut choice = String::new();
        io::stdin().read_line(&mut choice)
            .expect("Errror reading input");
    
        choice = choice.trim().to_string();

        match choices.contains(&choice.as_str()) {
            true => return choice,
            false => warn("Invalid input."),
        };

    }

}