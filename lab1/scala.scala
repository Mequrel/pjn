import scala.io.Source
import scala.util.parsing.combinator.RegexParsers
import scala.util.matching.Regex

class WordTokenizer extends RegexParsers {
  override protected val whiteSpace: Regex = "".r // don't skip whitespaces

  private val wordParser = """[^\p{Punct}\p{Space}]+""".r
  private val noiseParser = """\p{Punct}""".r | """\p{Space}""".r

  private val words: Parser[List[String]] = (noiseParser*) ~>(((wordParser <~ (noiseParser+)) | wordParser)*)  <~ (noiseParser*)

  def parseWords(input: String): List[String] = parseAll(words, input) match {
    case Success(result, _) => result
    case failure: NoSuccess => throw new Exception(failure.msg)
  }
}

object WordCounter {
  val tokenizer = new WordTokenizer

  def extractWords(line: String) : List[String] = {
    // println(line)
    tokenizer.parseWords(line)
  }

  def main(args: Array[String]) {
    val words = for {
      line <- Source.fromFile(args(0)).getLines()
      word <- extractWords(line)
    } yield word

    // to lower 

    val counted = words.toSeq
                       .map(_.toLowerCase)
                       .groupBy(identity)
                       .map(entry => (entry._1, entry._2.size))
                       .toList.sortBy(- _._2)

    counted.foreach(word => println(word._1 + " " + word._2))
  }
}
