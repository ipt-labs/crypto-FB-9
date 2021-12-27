use std::fs;

use crate::util::Alphabet;

mod calculation;
mod util;
mod vigenere;

fn main() {
    println!("*Task 1-2*");
    let mut range = (2..=5).collect::<Vec<_>>();
    range.extend(10..=20);
    let text = fs::read_to_string("text.txt").unwrap();
    for key_len in range {
        let key = Alphabet::global().get_random_key(key_len);
        let encrypted_text = vigenere::encrypt(text.clone(), &key);
        println!("key: {}", key.into_iter().collect::<String>());
        println!("encrypted text: {}", encrypted_text);
        println!(
            "coincidence: {}",
            calculation::calc_coincidence(encrypted_text.chars())
        );
    }
    println!("*Task 3*");
    let encrypted_text = fs::read_to_string("encrypted.txt").unwrap();
    let (map, (length, coincidence)) = vigenere::crack_len(encrypted_text.clone());
    println!("max coincidence: {}", coincidence);
    println!("length {}:", length);
    println!("coincidence indexes: {:?}", map);
    let keys = vigenere::crack_keys(encrypted_text.clone(), length);
    println!("Possible keys: {:?}", keys);
    let decrypted = vigenere::decrypt(encrypted_text, "экомаятникфуко".to_string());
    println!("Decrypted text: {}", decrypted);
}
