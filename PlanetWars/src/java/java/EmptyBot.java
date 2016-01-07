package java;

import java.planetWarsAPI.Bot;
import java.planetWarsAPI.GameClient;
import java.planetWarsAPI.Planet;
import java.planetWarsAPI.PlanetWars;

/**
 * EmptyBot
 * A skeleton for a bot.
 * <p>
 * Only contains the basic layout for your bots.
 * All your bots should probably start with this template.
 *
 * @author Jur van den Berg
 * @version 2.1
 */
public class EmptyBot implements Bot {

    /**
     * Function that gets called every turn.
     * This is where you add your implementation
     *
     * @param pw The game state
     */
    public void doTurn(PlanetWars pw) {

        //notice that a PlanetWars object called pw is passed as a parameter which you could use
        //if you want to know what this object does, then read PlanetWars.java

        //create a source planet, if you want to know what this object does, then read Planet.java
        Planet source = null;

        //create a destination planet
        Planet dest = null;

        //(1) implement an algorithm to determine the source planet to send your ships from
        source = determineSrc();

        //(2) implement an algorithm to determine the destination planet to send your ships to
        dest = determineDest();

        //(3) Attack
        if (source != null && dest != null) {
            pw.issueOrder(source, dest);
        }
    }

    public Planet determineSrc(){

        return null;
    }

    public Planet determineDest(){

        return null;
    }


    public static void main(String[] args) {
        GameClient.run(new EmptyBot());
    }
}
