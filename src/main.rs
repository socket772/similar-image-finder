#![allow(clippy::needless_return)]
use dssim::DssimImage;
use image;
use image_compare;
use std::{
    env::args,
    fs::File,
    io::BufReader,
    sync::{Arc, Mutex},
    thread, vec,
};
use walkdir::WalkDir;

struct Immagini {
    vettore_immagini: Vec<String>,
    posizione: usize,
    base_image: image::ImageReader<BufReader<File>>,
}

fn main() {
    let args: Vec<String> = args().collect();

    if args.len() != 3 {
        return;
    }

    let lista_files = WalkDir::new(args[1].clone());
    let mut vettore: Vec<String> = vec![];

    for elemento in lista_files.into_iter().flatten() {
        if elemento.path().is_file() {
            vettore.push(elemento.path().to_str().unwrap().to_string());
        }
    }

    let dati_condivisi = Immagini {
        vettore_immagini: vettore,
        posizione: 0,
        base_image: image::ImageReader::open(args[2].clone()).unwrap(),
    };

    let numero_immagini = dati_condivisi.vettore_immagini.len();

    if dati_condivisi.vettore_immagini.is_empty() {
        // println!("Niente immagini");
        return;
    }

    let mutex_lock: Arc<Mutex<Immagini>> = Arc::new(Mutex::new(dati_condivisi));

    let mut thread_vector: Vec<thread::JoinHandle<()>> = vec![];

    for _thread_id in 0..16 {
        let mutex_lock = mutex_lock.clone();
        // println!("Thread {} iniziato", thread_id);

        thread_vector.push(thread::spawn(move || {
            for _ in 0..numero_immagini {
                if thread_operation(mutex_lock.clone(), numero_immagini) == 1 {
                    break;
                }
            }
            // println!("Thread '{}' ha finito", thread_id);
        }));
    }

    for thread_element in thread_vector {
        let _ = thread_element.join();
    }
}

fn thread_operation(mutex_lock: Arc<Mutex<Immagini>>, numero_immagini: usize) -> i32 {
    // Creo l'istanza per il calcolo
    let dssim = dssim::new();

    // prendo il lucchetto mutex_lock
    let mut dati_condivisi = mutex_lock.lock().unwrap();

    // Copio le variabili che mi servono dalla struct
    let posizione_temp = dati_condivisi.posizione;
    let vettore_immagini_temp = dati_condivisi.vettore_immagini.clone();
    let base_image = dati_condivisi.base_image;

    // Controllo se ci sono altre canzoni da convertire
    if posizione_temp >= numero_immagini {
        drop(dati_condivisi);
        return 1;
    }
    // Aumento di 1 il contatore globale
    dati_condivisi.posizione += 1;
    drop(dati_condivisi);

    // Estraggo il nome della canzione
    let nome_immagine = vettore_immagini_temp[posizione_temp].clone();
    // println!("{}", nome_immagine);
    let immagine_target = image::ImageReader::open(nome_immagine.clone()).unwrap();

    let result = image_compare::rgb_hybrid_compare(&base_image, &immagine_target).unwrap();

    println!("{:?};{}", result, nome_immagine);

    return 0;
}
