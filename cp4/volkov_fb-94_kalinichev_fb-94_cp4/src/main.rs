extern crate num_bigint_dig as num_bigint;

use num_bigint::{BigInt, BigUint, ModInverse, RandBigInt, RandomBits, ToBigInt, ToBigUint};
use num_integer::Integer;
use num_traits::Num;
use rand::Rng;

fn miller_rabin(p: BigInt, k: usize) -> bool {
    let mut rng = rand::thread_rng();
    let zero = 0.to_bigint().unwrap();
    let one = 1.to_bigint().unwrap();
    let two = 2.to_bigint().unwrap();

    let p_minus_one = &p - &one;
    let mut d = p_minus_one.clone();
    let mut s = zero.clone();

    while &d % &two == one {
        d /= &two;
        s += &one;
    }

    'l: for _ in 0..k {
        let x = rng.gen_bigint_range(&two, &d);
        let mut v = x.modpow(&d, &p);
        if &v == &one {
            continue 'l;
        }
        let mut i = zero.clone();
        while &i < &s {
            v = (v.clone() * &v) % &p;
            if &v == &p_minus_one {
                continue 'l;
            }
            i += &one;
        }
        return false;
    }
    true
}

fn gen_prime() -> BigUint {
    let mut rng = rand::thread_rng();
    loop {
        let signed: BigUint = rng.sample(RandomBits::new(256));
        if miller_rabin(signed.to_bigint().unwrap(), 100) {
            return signed;
        }
    }
}

fn gen_pair() -> (BigUint, BigUint) {
    (gen_prime(), gen_prime())
}

fn gen_compatible_pair(p: BigUint, q: BigUint) -> (BigUint, BigUint) {
    let n = p * q;
    loop {
        let (p, q) = gen_pair();
        if n <= &p * &q {
            return (p, q);
        }
    }
}

#[derive(Debug)]
struct User {
    name: String,
    n: BigUint,
    exp: BigUint,
    d: BigUint,
    received_exp: Option<BigUint>,
    received_n: Option<BigUint>,
}

impl User {
    fn new(name: String, p: BigUint, q: BigUint) -> Self {
        let one = 1.to_biguint().unwrap();
        let totient = (&p - &one) * (&q - &one);
        let mut rng = rand::thread_rng();
        loop {
            let exp = rng.gen_biguint_range(&2.to_biguint().unwrap(), &totient);
            if &exp.gcd(&totient) == &one {
                println!("Create user: {}", &name);
                println!("p: {}\nq: {}", &p, &q);
                println!("exp: {}", &exp);
                let n = p * q;
                let d = exp
                    .clone()
                    .mod_inverse(&totient)
                    .unwrap()
                    .to_biguint()
                    .unwrap();
                println!("n: {}", &n);
                println!("d: {}", &d);
                return User {
                    name,
                    n,
                    exp,
                    d,
                    received_exp: None,
                    received_n: None,
                };
            }
        }
    }

    fn send_message(&self, text: String) -> String {
        let m = BigUint::from_bytes_be(text.as_bytes());
        let c = m
            .modpow(
                &self.received_exp.as_ref().unwrap(),
                &self.received_n.as_ref().unwrap(),
            );
        let encrypted = c.to_str_radix(16u32);
        println!(
            "{} send message: {}\nencrypted_text: {}\nencrypted_integer: {}\n",
            &self.name, text, &encrypted, c
        );
        encrypted
    }

    fn receive_message(&self, text: String) -> String {
        let c = BigUint::from_str_radix(&text, 16u32).unwrap();
        let dec = c.modpow(&self.d, &self.n);
        let decrypted = String::from_utf8(dec.to_bytes_be()).unwrap();
        println!(
            "{} receive message: {}\ndecrypted_text: {}\ndecrypted_integer: {}",
            &self.name, text, &decrypted, dec
        );
        decrypted
    }

    fn sing_message(&self, text: String) -> (String, String) {
        let m = BigUint::from_bytes_be(&text.as_bytes());
        let signature = m.modpow(&self.d, &self.n).to_str_radix(16u32);
        println!(
            "{} sing message: {}\nsignature: {}\n",
            &self.name, text, &signature
        );
        (signature, text)
    }

    fn verify_signature(&self, signature: String, message: String) -> bool {
        let m = BigUint::from_str_radix(&signature, 16u32).unwrap();
        let m = m
            .modpow(
                &self.received_exp.as_ref().unwrap(),
                &self.received_n.as_ref().unwrap(),
            )
            .to_bytes_be();
        let message1 = String::from_utf8(m).unwrap();
        if message == message1 {
            println!(
                "{} successfully verify signature {} for message: {}",
                &self.name, &signature, &message
            );
            true
        } else {
            false
        }
    }

    fn send_key(&self) -> (BigUint, BigUint) {
        println!("{} send key", &self.name);
        (self.exp.clone(), self.n.clone())
    }

    fn receive_key(&mut self, key: (BigUint, BigUint)) {
        println!("{} receive key", &self.name);
        self.received_exp = Some(key.0);
        self.received_n = Some(key.1);
    }
}

fn main() {
    let (p, q) = gen_pair();
    let (p1, p2) = gen_compatible_pair(p.clone(), q.clone());

    let mut alice = User::new("Alice".to_string(), p, q);
    let mut bob = User::new("Bob".to_string(), p1, p2);

    bob.receive_key(alice.send_key());
    alice.receive_key(bob.send_key());

    let encrypted = alice.send_message("Hello Bob!".to_string());
    bob.receive_message(encrypted);

    let (signature, message) = alice.sing_message("Bob check my sign".to_string());
    bob.verify_signature(signature, message);
}
