use once_cell::sync::OnceCell;
use rand::seq::IteratorRandom;
use std::str::Chars;

static ALPHABET: OnceCell<Alphabet> = OnceCell::new();

pub struct Alphabet(Vec<char>);

impl Alphabet {
    pub fn global() -> &'static Alphabet {
        ALPHABET.get_or_init(|| Alphabet(('а'..='я').collect::<Vec<_>>()))
    }

    pub fn get_index(&self, ch: &char) -> usize {
        self.0.iter().position(|c| c == ch).unwrap()
    }

    pub fn get_char(&self, index: usize) -> &char {
        self.0.get(index).unwrap()
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }

    pub fn get_random_key(&self, key_len: usize) -> Vec<&char> {
        self.0
            .iter()
            .choose_multiple(&mut rand::thread_rng(), key_len)
    }
}

pub fn create_blocks(chars: Chars, key_len: usize) -> impl Iterator<Item = Vec<char>> + '_ {
    (0..key_len).map(move |size| {
        let iter = chars.clone().into_iter();
        if key_len == 0 {
            iter.collect::<Vec<_>>()
        } else {
            iter.skip(size).step_by(key_len).collect::<Vec<_>>()
        }
    })
}
