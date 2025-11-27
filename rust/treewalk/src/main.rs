use std::env;
use std::fs;
use std::io::{self, BufRead, Write};
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() > 2 {
        eprintln!("Usage: treewalk [script]");
        process::exit(64);
    } else if args.len() == 2 {
        run_file(&args[1]).unwrap_or_else(|err| {
            eprintln!("Error reading file: {}", err);
            process::exit(1);
        });
    } else {
        run_prompt().unwrap_or_else(|err| {
            eprintln!("Error: {}", err);
            process::exit(1);
        });
    }
}

fn run_file(path: &str) -> io::Result<()> {
    let _ = fs::read_to_string(path)?;
    // run(contents);
    Ok(())
}

fn run_prompt() -> io::Result<()> {
    let stdin = io::stdin();
    let mut reader = stdin.lock();
    let mut line = String::new();
    
    loop {
        print!("> ");
        io::stdout().flush()?;
        
        line.clear();
        let bytes_read = reader.read_line(&mut line)?;
        
        if bytes_read == 0 {
            break; // EOF
        }
        
        // run(line.trim());
    }
    
    Ok(())
}