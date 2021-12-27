use ordered_float::OrderedFloat;
use std::collections::HashMap;

use crate::util::Alphabet;
use crate::{calculation, util};

pub fn encrypt(text: String, key: &Vec<&char>) -> String {
    text.chars()
        .enumerate()
        .map(|(i, ch)| {
            let letter_index = Alphabet::global().get_index(&ch);
            let key_char = key.get(i.rem_euclid(key.len())).unwrap();
            let key_index = Alphabet::global().get_index(key_char);
            Alphabet::global()
                .get_char((letter_index + key_index).rem_euclid(Alphabet::global().len()))
        })
        .collect()
}

pub fn crack_len(text: String) -> (HashMap<usize, f32>, (usize, f32)) {
    let chars = text.chars();
    let mut map = HashMap::new();
    for key_len in 1..=20 {
        let mut coincidence = util::create_blocks(chars.clone(), key_len)
            .map(|chars| calculation::calc_coincidence(chars.into_iter()))
            .fold(0f32, |coincidence_sum, coincidence| {
                coincidence_sum + coincidence
            });
        coincidence /= key_len as f32;
        map.insert(key_len, coincidence);
    }
    (
        map.clone(),
        map.into_iter()
            .max_by_key(|(_, coincidence)| OrderedFloat(coincidence.clone()))
            .unwrap(),
    )
}

pub fn crack_keys(text: String, key_len: usize) -> HashMap<char, String> {
    let letters = vec!['о', 'а', 'у'];
    let chars = text.chars();
    let mut map = HashMap::new();
    for letter in letters {
        let possible_key = util::create_blocks(chars.clone(), key_len)
            .map(|chars| calculation::calc_frequency(chars.into_iter()))
            .map(|frequencies| {
                let most_frequent = frequencies
                    .into_iter()
                    .max_by_key(|(_, frequency)| OrderedFloat(frequency.clone()))
                    .unwrap()
                    .0;
                let encoded_index = Alphabet::global().get_index(&most_frequent) as isize;
                let letter_index = Alphabet::global().get_index(&letter) as isize;
                let decoded_index = (encoded_index - letter_index)
                    .rem_euclid(Alphabet::global().len() as isize)
                    as usize;
                Alphabet::global().get_char(decoded_index)
            })
            .collect::<String>();
        map.insert(letter, possible_key);
    }
    map
}

pub fn decrypt(text: String, key: String) -> String {
    let key = key.chars().collect::<Vec<_>>();
    text.chars()
        .enumerate()
        .map(|(index, letter)| {
            let encoded_index = Alphabet::global().get_index(&letter) as isize;
            let key_letter = key.get(index.rem_euclid(key.len())).unwrap();
            let key_index = Alphabet::global().get_index(key_letter) as isize;
            let decoded_index =
                (encoded_index - key_index).rem_euclid(Alphabet::global().len() as isize) as usize;
            Alphabet::global().get_char(decoded_index)
        })
        .collect::<String>()
}
