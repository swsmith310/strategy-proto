package main;
import (
  "fmt"
  "io"
  "net/http"
  "strconv"
);

var activePlayers = 0;

func WriteAndPrint(w http.ResponseWriter, text string) {
    io.WriteString(w,text + "\n");
    fmt.Println(text);
}

func getRoot(w http.ResponseWriter, r *http.Request){
  fmt.Printf("/ route\n");
  io.WriteString(w,"STRATEGY PROTO SERVER v0.0.1a\n");

  /*if (r.URL.Query().Has("increment")) {
    i, err := strconv.Atoi(r.URL.Query().Get("increment"));
    if (err != nil) {
      return;
    }
    x += i;
  }
  io.WriteString(w,fmt.Sprint(x) + "\n");*/

  if (r.URL.Query().Has("player")) {
    p := r.URL.Query().Get("player");
    if (r.URL.Query().Has("logout")) {
      activePlayers--;
      WriteAndPrint(w,fmt.Sprint(p + " has left the game!"));
      WriteAndPrint(w,fmt.Sprint("Current active players: " + strconv.Itoa(activePlayers)));
      return;
    }
    if (r.URL.Query().Has("clicked")) {
      WriteAndPrint(w,fmt.Sprint(p + " was clicked!"));
      return;
    }
    activePlayers++;
    WriteAndPrint(w,fmt.Sprint(p + " has joined the game!"));
    WriteAndPrint(w,fmt.Sprint("Current active players: " + strconv.Itoa(activePlayers)));
    return;
  }
}

func main() {
  mux := http.NewServeMux();
  mux.HandleFunc("/", getRoot);
  err := http.ListenAndServe(":8080", mux);
  if (err != nil) {
    return;
  }
}
