# Sanapeli

Sanapelissä pelaajan on tarkoitus arvata mahdollisimman monta sanaa kolmen minuutin sisällä. Aluksi peli paljastaa vain sanan pituuden, ja jokaisen arvauksen jälkeen peli näyttää mitkä kirjaimet osuivat sanassa oikeaan, mitkä olivat oikeita kirjaimia mutta väärällä paikalla, ja mitkä kirjaimet eivät kuulu ollenkaan sanaan. Pelissä on useita teemoja joilla peliä voi pelata. Ylläpitäjä voi hallita sovelluksessa olevia teemoja ja niihin liittyviä sanoja. Sovellusta voi kokeilla osoitteessa https://wordgame-tsoha.herokuapp.com/ .

## Välipalautus 3 19.6.2022

### Sovelluksen tilanne

Sovellukseen on toteutettu kaikki toiminnot, ja sitä on parannettu viime välipalautuksen palautteen perusteella. Käyttäjäkokemusta on parennettu niin, että sovellusta pitäisi pystyä käyttämään selkeästi ilman erillistä dokumentaatiota. Sen verran voisi tosin tarkentaa, että ylläpito-ominaisuuksia testatakseen, tulee rekisteröityä tunnus, jolla on valittu "Ylläpitäjän oikeudet." Muuten sovelluksesta pitäisi pääosin puuttua enää yksityiskohtia ja hienosäätöä. Keskeiset muutokset ovat:
 - Parhaat tulokset ja kirjautuminen toteutettu.
 - Navigointia selkeytetty: lisätty navigointipalkki ja 'breadcrumbs'.
 - Sivuille lisätty opastavia tekstejä.
 - Ulkoasua selkeytetty hieman.
 - Koodin rakennetta selkeytetty. Pitkät tiedostot on hajautettu useaan tiedostoihin omiin moduuleihinsa. Moduulit paljastavat vain tarpeelliset symbolit ulos päin ja sisäinen toteutus on kapsuloitu. Jokaisella tiedostolla on selkeämmin oma yksittäinen vastuunsa, esim. routes -tiedostot eivät sisällä sovelluslogiikkaa, vaan ovat vastuussa pyyntöjen parsimisista ja vastausten luonnista.

### Sovelluksen rakenteesta

 - Python-koodi on hakemistoissa `wordgame`, `wordgame/admin`, `wordgame/auth`, `wordgame/db` ja `wordgame/game`.
 - Peli sisältää jonkin verran javascript-koodia, ja se on tiedostossa `static/js/game.js`. Muut js-tiedostot ovat käytettyjä kirjastoja.

## Välipalautus 2 5.6.2022

### Sovelluksen tilanne

Sovellukseen on toteutettu keskeiset toiminnot, eli peliä voi pelata haluamallaan teemalla ja peliin liittyviä sanoja ja teemoja voi hallita. Sovelluksesta puuttuu kokonaan tunnuksen luominen ja kirjautuminen, ja parhaiden tulosten lista. Myös ulkoasu ja käytettävyys on keskeneräinen.

### Miten testata?

Pääsivulla pelin voi aloittaa suoraan valitsemalla teeman "Aloita peli" laatikosta. Ylläpito-sivulle pääsee ylläpito napista.

Pelin aloitettua aika alkaa juoksemaan heti. Sivulla on jokaiselle kirjaimelle oma laatikko ja sanaa voi alkaa kirjoittamaan näppäimistöllä suoraan. Kun laatikot ovat täynnä, peli kertoo saman tien miten arvaus meni. Oikeat kirjaimet värjäytyy vihreäksi, kokonaan väärät punaiseksi, ja osittain oikeat oranssiksi. Kirjainlaatikoiden oikealla puolella näkyy kuinka monta pistettä oikeasta arvauksesta saa. Jos sanan arvaa oikein kolmen ensimmäisen aikana, pisteitä saa 10, ja sen jälkeen pistemäärä tippuu jokaisen vihjeen jälkeen yhdellä. Oikean arvauksen jälkeen peli antaa uuden sanan arvattavaksi. Ajan loputtua pelaaja näkee kuinka monta pistettä yhteensä sai.

Ylläpidossa on kolme erilaista hallintasivua. "Lisää sanoja" sivulla peliin voi lisätä useita sanoja kerralla. Sanalistaan jokainen sana tulee omalle rivilleen. Halutessa sanat voi lisätä suoraan johonkin teemaan, mutta ne voi myös lisätä teemoihin muilla hallintasivuilla myöhemmin.

"Hallitse teemoja" sivulla ylläpitäjä voi nähdä yhteenvedon pelissä olevista teemoista ja lisätä uusia teemoja. Teeman nimeä klikkaamalla voi tarkastella teeman tarkempia tietoja ja toimintoja. Tällä hetkellä teeman sivulla voi nähdä teemaan liittyvän sanalistan ja koko teeman voi poistaa. **HUOM:** Destruktiivisilla operaatioilla ei ole tällä hetkellä erillistä konfirmaatiota. Teema esimerkiksi tuhoutuu saman tien "Poista teema" napista. Ole siis varovainen käsitellessä sivua. Mutta testaa toki poistotoimintoa vaikka itse luomallesi teemalle.

"Hallitse sanoja" sivulla näkyy yhteenveto kaikista pelissä olevista sanoista ja mihin teemoihin sanat kuuluvat. Useita sanoja voi poistaa kerralla valitsemalla ne poistettavaksi ja painamalla "Poista valitut" nappia. Sanoja voi myös lisätä ja poistaa teemoista checkboxeja painamalla. Muutos tallentuu saman tien kantaan kun arvoa muuttaa.

## Alkuperäinen konsepti

### Kuvaus

Sovellus on internetissä suositusta sanapelistä inspiraation saanut peli. Pelaajalle annetaan arvattavaksi sanoja, jotka tulee arvata viidellä yrittämällä mahdollisimman nopeasti. Aluksi pelaaja näkee vain sanan pituuden, ja jokaisen arvausyrityksen jälkeen hänpelaaja saa vihjeitä seuraavaa arvausta varten. Vihjeet näyttävät mitkä kirjaimet arvauksesta olivat oikein oikealla paikalla, mitkä kirjaimet löytyy sanasta mutta ovat väärällä paikalla ja mitä kirjaimia ei löydy sanasta ollenkaan. Peliaikaa on kaksi minuuttia, ja tuona aikana pelaajan tulee arvata niin monta sanaa kuin ehtii. Pelissä on eri teemoja, johon kuuluvia sanoja voi arvuutella.

### Sovelluksen ominaisuuksia:
 - Käyttäjä voi luoda tunnuksen ja kirjautua sisään.
 - Pelaaja voi pelata sanapelin haluamallaan teemalla ja lopuksi nähdä pelistä ansaitun pistemäärän.
 - Pelaaja voi nähdä listan kaikkien aikojen parhaista tuloksista teemoittain. Pelaaja voi nähdä myös omat parhaat suoritukset teemoittain.
 - Ylläpitäjä voi lisätä sanoja peliin, ja valita mihin teemoihin lisätyt sanat kuuluvat - sama sana vai kuulua useaan teemaan.
 - Ylläpitäjä voi lisätä ja poistaa pelistä teemoja. Teemat voi aktivoida pelattavaksi tai deaktivoida. Teemojen sanalistoja voi selata ja yksittäisiä sanoja voi lisätä tai poistaa.

