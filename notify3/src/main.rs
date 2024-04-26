mod utils;

fn main() {

  let command = "https://www.zanzi.dev";

  match utils::reqget(command) {
    Ok(Some(status)) => utils::info(status),
    Ok(None) => utils::warn("No response"),
    Err(err) => utils::warn(err),
  };

}
