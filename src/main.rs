extern crate piston_window;

use piston_window::*;
use std::time::{Instant, Duration};

#[derive(Debug, Clone)]
struct Snake {
    body: Vec<[i32; 2]>,
    direction: Direction,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

impl Snake {
    fn new() -> Self {
        Snake {
            body: vec![[5, 5], [5, 6], [5, 7]],
            direction: Direction::Right,
        }
    }

    fn move_forward(&mut self) {
        let mut new_head = self.body[0];
        match self.direction {
            Direction::Up => new_head[1] = (new_head[1] - 1 + 20) % 20,
            Direction::Down => new_head[1] = (new_head[1] + 1) % 20,
            Direction::Left => new_head[0] = (new_head[0] - 1 + 20) % 20,
            Direction::Right => new_head[0] = (new_head[0] + 1) % 20,
        }
        self.body.insert(0, new_head);
        self.body.pop();
    }

    fn change_direction(&mut self, new_direction: Direction) {
        if new_direction != self.direction.opposite() {
            self.direction = new_direction;
        }
    }

    fn eat(&mut self) {
        let tail = *self.body.last().unwrap_or(&[0, 0]);
        self.body.push(tail);
    }

    fn check_collision(&self) -> bool {
        let head = self.body.first().cloned().unwrap_or([0, 0]);
        self.body.iter().skip(1).any(|&x| x == head)
    }
}

impl Direction {
    fn opposite(&self) -> Direction {
        match *self {
            Direction::Up => Direction::Down,
            Direction::Down => Direction::Up,
            Direction::Left => Direction::Right,
            Direction::Right => Direction::Left,
        }
    }
}

fn generate_random_position(snake_body: &[[i32; 2]]) -> [i32; 2] {
    use rand::seq::SliceRandom;

    let all_positions: Vec<[i32; 2]> = (0..20).flat_map(|x| (0..20).map(move |y| [x, y])).collect();
    let empty_positions: Vec<[i32; 2]> = all_positions
        .into_iter()
        .filter(|&pos| !snake_body.contains(&pos))
        .collect();

    if let Some(&chosen_position) = empty_positions.choose(&mut rand::thread_rng()) {
        chosen_position
    } else {
        panic!("No empty position available for food!");
    }
}

fn main() {
    let mut window: PistonWindow =
        WindowSettings::new("Snake Game", [400, 400]).exit_on_esc(true).build().unwrap();

    let mut snake = Snake::new();
    
    let mut food = generate_random_position(&snake.body);

    let mut last_update = Instant::now();
    let update_duration = Duration::from_millis(100); // Snake speed

    while let Some(e) = window.next() {
        if let Some(Button::Keyboard(key)) = e.press_args() {
            match key {
                Key::Up => snake.change_direction(Direction::Up),
                Key::Down => snake.change_direction(Direction::Down),
                Key::Left => snake.change_direction(Direction::Left),
                Key::Right => snake.change_direction(Direction::Right),
                _ => {}
            }
        }

        let elapsed_time = last_update.elapsed();
        if elapsed_time >= update_duration {
            last_update = Instant::now();
            snake.move_forward();

            if snake.body[0] == food {
                snake.eat();
                food = generate_random_position(&snake.body);
            }

            if snake.check_collision() {
                println!("Game Over!");
                break;
            }
        }

        window.draw_2d(&e, |c, g, _| {
            clear([0.0, 0.0, 0.0, 1.0], g);

            for &block in &snake.body {
                rectangle(
                    [0.0, 1.0, 0.0, 1.0],
                    [block[0] as f64 * 20.0, block[1] as f64 * 20.0, 20.0, 20.0],
                    c.transform,
                    g,
                );
            }

            rectangle(
                [1.0, 0.0, 0.0, 1.0],
                [food[0] as f64 * 20.0, food[1] as f64 * 20.0, 20.0, 20.0],
                c.transform,
                g,
            );
        });
    }
}
