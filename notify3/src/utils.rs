use std::{io::{self, Write}, process::exit};

static INFO  : &str = "\x1b[92m\x1b[1m[ INFO  ]:\x1b[0m ";
static INPUT : &str = "\x1b[94m\x1b[1m[ INPUT ]:\x1b[0m ";
static WARN  : &str = "\x1b[93m\x1b[1m[ WARN  ]:\x1b[0m ";
static ERROR : &str = "\x1b[91m\x1b[1m[ ERROR ]:\x1b[0m ";

pub fn info<T:std::fmt::Display>(msg : T) {
    println!("{INFO}{msg}");
}

pub fn warn<T:std::fmt::Display>(msg: T) {
    println!("{WARN}{msg}");
}

pub fn error<T:std::fmt::Display>(msg: T) {
    println!("{ERROR}{msg}");
    exit(1);
}

pub fn input<T:std::fmt::Display>(msg : T, choices : &[&str]) -> String {

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