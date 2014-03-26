import java.util.Scanner
import scala.collection.JavaConverters._
import java.io.File

object WordCountEasy {
  def main(args: Array[String]) {
    val file: java.util.Iterator[String] = new Scanner(new File(args(0)))
                .useDelimiter("(\\p{Punct}|\\p{Space})+")

    val counted = file.asScala.toStream
                       .map(_.toLowerCase)
                       .groupBy(identity)
                       .map(entry => (entry._1, entry._2.size))
                       .toSeq.sortBy(- _._2)

    counted.foreach(word => println(word._1 + " " + word._2))
  }
}