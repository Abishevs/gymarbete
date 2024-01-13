extern crate rand;
extern crate rayon;
use rand::seq::SliceRandom;
use rayon::prelude::*;
use rand::Rng;
use std::fs::File;
use std::io::Write;
use std::time::{Duration, Instant};

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

struct PileShuffle;
impl  ShufflingAlgorithm for PileShuffle {
    fn name(&self) -> &str {
        "soc_pile_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        const BIN_COUNTS:usize = 8;
        const MAX_CARDS_PER_BIN:usize = 10;


        let mut bins: Vec<Vec<Card>> = vec![Vec::new(); BIN_COUNTS];

        let mut rng = rand::thread_rng();
        for &card in deck.iter() {
            loop {
                let random_bin = rng.gen_range(0..BIN_COUNTS);
                if bins[random_bin].len() < MAX_CARDS_PER_BIN { 
                    // put the cards in random bins
                    bins[random_bin].push(card);
                    break;
                }
            }
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

struct FixedRiffle;
impl ShufflingAlgorithm for FixedRiffle{
    fn name(&self) -> &str {
        "fixed_riffle_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        let mut deck_vec: Vec<Card> = Vec::with_capacity(52);
        let mut deck_half_1: Vec<Card> = Vec::new();
        let mut deck_half_2: Vec<Card> = Vec::new();

        let mut card_count = 1;
        for &card in deck.iter() {
            if card_count <= (deck.len() / 2) {
                deck_half_1.push(card);
                card_count += 1;
            } else {
                deck_half_2.push(card);
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
        // println!("{:?}", deck);
    }
}

struct WheelSpiny;
impl  ShufflingAlgorithm for WheelSpiny {
    fn name(&self) -> &str {
        "v1_wheel_spinie"
    }

    fn shuffle(&self, deck: &mut Deck) {
        let mut rng = rand::thread_rng();

        // Run riffle shuffle to create random indexs.
        let mut random_indexs = (0..52).collect::<Vec<_>>();
        random_indexs.shuffle(&mut rng);
        
        let mut wheel_slots: Vec<Card> = vec![0; 52];
        // map index to an slot on the wheel.
        for &card in deck.iter() {
            if let Some(index) = random_indexs.pop() {
                wheel_slots[index] = card;
            }
        }

        // take all the slots from the beginning and place them in it's new deck.
        let mut deck_position = 0;
        for card in wheel_slots {
            deck[deck_position] = card;
            deck_position += 1;
        }

        // println!("{:?}", deck);
    }
}

struct GSRRiffle;
impl ShufflingAlgorithm for GSRRiffle{
    fn name(&self) -> &str {
        "gsr_riffle_shuffle"
    }

    fn shuffle(&self, deck: &mut Deck){
        let mut deck_vec: Vec<Card> = Vec::with_capacity(52);
        let mut deck_half_1: Vec<Card> = Vec::new();
        let mut deck_half_2: Vec<Card> = Vec::new();
        
        let mut card_count = 1;
        for &card in deck.iter() {
            if card_count <= (deck.len() / 2) {
                deck_half_1.push(card);
                card_count += 1;
            } else {
                deck_half_2.push(card);
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

            } else {
                if let Some(card) = deck_half_2.pop() {
                    deck_vec.insert(0, card);
                }
            }
        }

        let mut deck_position = 0;
        for card in deck_vec {
            deck[deck_position] = card;
            deck_position += 1;
        }

        // println!("{:?}", deck);
    }
}

fn generate_dataset(algorithm: &Box<dyn ShufflingAlgorithm>, runs: i32 ) -> (Dataset, Duration) {
    let mut dataset: Dataset = vec![[0; DECK_SIZE]; DATASET_LENGHT];
    for deck in dataset.iter_mut() { 
        // build out deck
        for i in 0..DECK_SIZE{
            deck[i] = i as Card;
        }
    }

    let mut total_duration = Duration::new(0, 0);
    for _ in 1..=runs{
        for deck in dataset.iter_mut() {
            let start = Instant::now();
            algorithm.shuffle(deck);
            let duration = start.elapsed();

            total_duration += duration;

        }
    }

    let avg_duration = total_duration / (DATASET_LENGHT as u32 * runs as u32);
    (dataset, avg_duration)
}

fn write_to_file(dataset: Dataset, file_name: &String) -> std::io::Result<()>{
    let flatten_dataset: Vec<Card> = dataset.into_iter().flatten().collect();
    let mut file = File::create(&file_name)?;

    file.write_all(&flatten_dataset)?;
    
    Ok(())
}

fn main() {
    let algorithms: Vec<Box<dyn ShufflingAlgorithm>> = vec![
        Box::new(PileShuffle),
        Box::new(WheelSpiny),
        Box::new(FixedRiffle),
        Box::new(GSRRiffle),
    ];

    const ITERATIONS:i32 = 10;
    
    // each algo simulation runs in parallel
    algorithms.par_iter().for_each(|algorithm| {
        // i will be used as runs
        let mut total_duration = Duration::new(0, 0);
        for runs in 1..=ITERATIONS {

            let (dataset, time) = generate_dataset(algorithm, runs);
            let file_name = format!("{}-{}.bin", algorithm.name(), runs);
            match write_to_file(dataset, &file_name) {
                Ok(_) => {
                    println!("File {} written succesfully", file_name); 
                    total_duration += time;
                    
                },
                Err(e) => eprintln!("Error writing to file {}: {}", file_name, e),

            }
        }
        let average_duration = total_duration / ITERATIONS as u32;

        let file_name = format!("{}_avg_time.txt", algorithm.name());
        match File::create(&file_name) {
            Ok(mut file) => {
                if let Err(e) = writeln!(file, "{}", average_duration.as_nanos()) {
                    eprintln!("Error writing average duration to file {}: {}", file_name, e);
                }
            },
            Err(e) => {
                eprintln!("Error creating file {}: {}", file_name, e);
            }
        }

    });
}
