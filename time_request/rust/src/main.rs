use std::net::{TcpStream};
// use std::io::{Read, Write};
// use std::str::from_utf8;

fn connect () {
    if let Ok(stream) = TcpStream::connect("dbl44.beuth-hochschule.de:21") {
        println!("Connection established:");
    } else {
        println!("Couldn't connect to server...");
    }
}

fn main () {
    let hostname = "dbl44.beuth-hochschule.de";
    let port = "21";
    connect();
}