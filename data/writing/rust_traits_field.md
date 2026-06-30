---
title: [Rust] Property with a type that implements a trait
description: How to have a struct member with type that implements a trait in Rust
priority: 95
date: 2023-02-25
---

# Struct member with type that implements a trait in Rust

I have found that it is not trivial (*for someone who is learning Rust, like me*) to have a struct which has an attribute whose type inherits from a trait. Such situation typically happens when defining the behavior of a callback.


First, let's define the types we will be working with.

<pre><code class="language-rust">/// Defines a trait
trait Callback {
    fn hello(&self);
}

/// A struct that contains some data.
/// In this case, Container contains a reference to an object that lives 
/// outside of this scopet. herefore we need to annotate the lifetime specyfier
struct Container<'a> {
    text: &'a str
}

// Let's define a constructor ...
impl <'a> Container <'a> {
   fn new(text: &'a str) -> Self {
       Self {text}
   } 
}

// Let's make our struct implement the trait `Callback`
impl <'a> Callback for Container <'a> {
    fn hello(&self) {
       println!("Hello: {}", self.text) ;
    } 
}
</code></pre>

Now, our goal is to create a new type <code>Boo</code> which has an attribute that implements <code>Callback</code> (but we don't care which class in particular). So, exactly like an Interface in Java. There are two ways to do this.

### Using generic types

Note that this way only works if the instance of the struct holding the callback (in this case <code>Boo</code>), only supports one kind of type of callback.

<pre><code class="language-rust">/// If you want another struct which has our trait as a field, this is one easy
/// approach. However, each instance of `Boo` will only be able to have only 1 
/// type of field `foo`.
struct Boo &lt;T: Callback&gt {
    foo: T
}

// The implementation of the struct with generic type is similar as for lifetime
// specifiers. 
impl&lt;T: Callback&gt; Boo&lt;T&gt; {
    fn new(cb: T) -> Self {
        Self {
            foo: cb
        }
    }
    
    /// A function that calls on our callback
    fn greet(&self) {
        self.foo.hello();
    }
}

fn main() {
    let c = Container::new("salut");
    c.hello();

    let b = Boo::new(c);
    b.greet();
}
</code></pre>

### Using <code>Box</code>

This approach is the better one if you want to change the callback during the lifetime of "foo". 

<pre><code class="language-rust">
/// Another approach, which allows to support different types on the same object,
/// is by using a box
struct DynamicBoo {
    // A box is a unique pointer
    foo: Box&lt;dyn Callback&gt;
}

impl DynamicBoo {
    fn new(cb: Box&lt;dyn Callback&gt;) -> Self {
        Self {
            foo: cb
        }
    }    
    
    fn greet(&self) {
        self.foo.hello();
    }
}

fn main() {
    let d = DynamicBoo::new(Box::new(Container::new("coucou")));
    d.greet();
}
</code></pre>


Here is the [link to rust playground](https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=0391a65d099601b3855c6732a63c6bec) with this code.
