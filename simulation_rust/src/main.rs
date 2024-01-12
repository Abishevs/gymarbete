extern crate rand;
extern crate rayon;
use rayon::prelude::*;
use std::fs::File;
use std::io::Write;
use rand::Rng;

const DATASET_LENGHT:usize = 3_248_700;
const DECK_SIZE:usize = 52;

type Card = u8;
type Deck = [Card; DECK_SIZE];
type Dataset = Vec<Deck>;

// generic trait for other shuffling algorithms
trait ShufflingAlgorithm: Send + Sync {
    fn name(&self) -> &str;
    fn shuffle(&self, deck: &mut Deck);
}

struct Algorithm1;
struct Algorithm2;
struct FixedRiffle;
struct GSRRiffle;

impl  ShufflingAlgorithm for Algorithm1{
    fn name(&self) -> &str {
        "v1_bin_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        const BIN_COUNTS:usize = 6;
        let mut bins: Vec<Vec<Card>> = vec![Vec::new(); BIN_COUNTS];

        let mut rng = rand::thread_rng();
        for &card in deck.iter() {
            let random_bin = rng.gen_range(0..BIN_COUNTS);
            // put the cards in random bins
            bins[random_bin].push(card);
        }

        let mut deck_position = 0;
        // Reassemble the deck
        for bin in bins {
            for card in bin {
                deck[deck_position] = card;
                deck_position += 1;
            }
        }
    }

}

impl  ShufflingAlgorithm for Algorithm2{
    fn name(&self) -> &str {
        "v2_bin_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        const BIN_COUNTS:usize = 6;
        let mut bins: Vec<Vec<Card>> = vec![Vec::new(); BIN_COUNTS];

        let mut rng = rand::thread_rng();
        for &card in deck.iter() {
            let random_bin = rng.gen_range(0..BIN_COUNTS);
            // put the cards in random bins
            bins[random_bin].push(card);
        }

        let mut deck_position = 0;
        // Reassemble the deck
        for bin in bins {
            for card in bin {
                deck[deck_position] = card;
                deck_position += 1;
            }
        }
    }

}

impl ShufflingAlgorithm for FixedRiffle{
    fn name(&self) -> &str {
        "fixed_riffle_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        let mut deck_vec: Vec<Card> = Vec::with_capacity(52);
        let mut deck_half_1: Vec<Card> = Vec::new();
        let mut deck_half_2: Vec<Card> = Vec::new();

        for _n in 0..26 {
            // put the fisrt half of the deck in a vec
            // deck_half_1.push(deck.iter().nth(0));
            if let Some(&card) = deck.iter().nth(0) {
                deck_half_1.push(card);
            }
        }

        for _n in 0..=26 {
            // put secound half of the deck in a vec
            if let Some(&card) = deck.iter().nth(0) {
                deck_half_1.push(card);
            }
        }

        let mut take_from_half_1 = true;
       
        while !deck_half_1.is_empty() && !deck_half_2.is_empty(){
            if take_from_half_1 {
                if let Some(card) = deck_half_1.pop() {
                    deck_vec.insert(0, card);
                    take_from_half_1 = false;
                }
            } else {
                if let Some(card) = deck_half_2.pop() {
                    deck_vec.insert(0, card);
                    take_from_half_1 = true;
                }
            }
        }

        let mut deck_position = 0;

        for card in deck_vec {
            deck[deck_position] = card;
            deck_position += 1;
        }
    }
}

impl ShufflingAlgorithm for GSRRiffle{
    fn name(&self) -> &str {
        "gsr_riffle_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        let mut deck_vec: Vec<Card> = Vec::with_capacity(52);
        let mut deck_half_1: Vec<Card> = Vec::new();
        let mut deck_half_2: Vec<Card> = Vec::new();

        for _n in 0..26 {
            // put the fisrt half of the deck in a vec
            // deck_half_1.push(deck.iter().nth(0));
            if let Some(&card) = deck.iter().nth(0) {
                deck_half_1.push(card);
            }
        }
        println!("{:?}", deck_half_1);

        for _n in 0..=26 {
            // put secound half of the deck in a vec
            if let Some(&card) = deck.iter().nth(0) {
                deck_half_1.push(card);
            }
        }

        let mut rng = rand::thread_rng();
        let mut rand_id;
        
        while !deck_half_1.is_empty() && !deck_half_2.is_empty() {
            rand_id = rng.gen_range(0.0..=1.0);
            if rand_id <= (deck_half_1.len() as f64)/((deck_half_1.len() as f64)+(deck_half_2.len() as f64)){
                if let Some(card) = deck_half_1.pop(){
                    deck_vec.insert(0, card);
                }   
            }
            else {
                if let Some(card) = deck_half_2.pop() {
                    deck_vec.insert(0, card);
                }
            }
        }
        println!("{:?}", deck_vec);

        let mut deck_position = 0;
        
        for card in deck_vec {
            deck[deck_position] = card;
            deck_position += 1;
        }
    }
}

fn generate_dataset(algorithm: &Box<dyn ShufflingAlgorithm>, runs: i32 ) -> Dataset{
    let mut dataset: Dataset = vec![[0; DECK_SIZE]; DATASET_LENGHT];
    for deck in dataset.iter_mut() { 
        // build out deck
        for i in 0..DECK_SIZE{
            deck[i] = i as Card;
        }
    }
    for _ in 1..=runs{
        for deck in dataset.iter_mut() {
            algorithm.shuffle(deck);
        }
    }

    dataset
}

fn write_to_file(dataset: Dataset, file_name: &String) -> std::io::Result<()>{
    let flatten_dataset: Vec<Card> = dataset.into_iter().flatten().collect();

    let mut file = File::create(&file_name)?;

    file.write_all(&flatten_dataset)?;
    
    Ok(())
}

fn main() {
    let algorithms: Vec<Box<dyn ShufflingAlgorithm>> = vec![
        Box::new(Algorithm1),
        // Box::new(Algorithm1),
        Box::new(Algorithm2),
        // Box::new(Algorithm2),
        Box::new(FixedRiffle),
        Box::new(GSRRiffle),
    ];

    // each algo simulation runs in parallel
    algorithms.par_iter().for_each(|algorithm| {
        // i will be used as runs
        for runs in 1..=10 {
            let dataset = generate_dataset(algorithm, runs);
            let file_name = format!("{}-{}.bin", algorithm.name(), runs);
            match write_to_file(dataset, &file_name) {
                Ok(_) => println!("File {} written succesfully", file_name),
                Err(e) => eprintln!("Error writing to file {}: {}", file_name, e),

            }
        }

    });
}
