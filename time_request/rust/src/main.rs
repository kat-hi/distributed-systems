use std::net::{TcpStream};
use std::io::{Read, Write};
use std::str::from_utf8;

fn main() {
    match TcpStream::connect("dbl44.beuth-hochschule.de:21"){
        Ok(mut Stream) => {
            println!("Connection established:")
        }
    }
}

