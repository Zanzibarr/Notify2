mod utils;

fn main() {
    utils::info("Hello, I have an important question for you.");
    let choice = utils::input("Do you like icecream?", &["y", "n"]);
    match choice.as_str() {
        "y" => utils::info("Really?!?!"),
        _ => utils::error("We can't be friends..."),
    }
    utils::info("I like it too!!!");
}