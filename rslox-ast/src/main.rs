use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() > 2 {
        println!("Usage: rslox [script]");
        std::process::exit(64);
    } else if args.len() == 2 {
        run_file(&args[1]);
    } else {
        run_prompt();
    }
}

fn run_file(path: &String) {
    let source = fs::read_to_string(path).expect("Something went wrong reading the file");
    println!("run_file: {}", source);
}

fn run_prompt() {
    loop {
        println!("> ");
        let mut input = String::new();
        std::io::stdin()
            .read_line(&mut input)
            .expect("Failed to read line");
        
        run(&input);
    }
}

fn run(source: &String) {
    println!("run: {}", source);
}
